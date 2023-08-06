import os, sys
import collections.abc
import shutil
import copy
import docker
import json
import tempfile
import uuid
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper



def dictionary_update( d, u ):
    for k, v in u.items():
        if isinstance( v, collections.abc.Mapping ):
            d[k] = dictionary_update( d.get(k, {}), v )
        else:
            d[k] = v
    return d



def prep_directory(dependencies):
    root_directory = os.path.join( tempfile.gettempdir(),f"ow-ci-helper-{str(uuid.uuid4())}" )
    while os.path.exists(root_directory):
        root_directory = os.path.join( tempfile.gettempdir(),  str(uuid.uuid4()) )
    os.mkdir(root_directory)

    volume_mounts = {}
    for dependency in dependencies:
        dependency_dir = os.path.join( root_directory, dependency )
        os.mkdir(dependency_dir)
        if dependency in 'model-registry':
            os.mkdir(os.path.join(dependency_dir, 'data-dir'))
            os.mkdir(os.path.join(dependency_dir, 'data-dir', 'models'))
        elif dependency in 'input-server':
            os.mkdir(os.path.join(dependency_dir, 'data-dir'))
            os.mkdir(os.path.join(dependency_dir, 'data-dir', 'inputs'))
            
        volume_mounts[dependency] = dependency_dir

    return root_directory, volume_mounts

def pull_image( client, image ):
    repo_name, tag = image.split(":")
    client.images.pull( repo_name, tag=tag )
    return

def make_mount_list(dependency, config, root_volume_directory):
    mounts = []
    config = copy.deepcopy(config)
    config.pop('docker')

    volume_path = os.path.join( root_volume_directory, dependency, 'config.yaml' )
    with open(volume_path, 'w') as f:
        f.write( yaml.dump(config, Dumper=Dumper) )

    mount_path = '/app/config.yaml'

    if dependency in ['input-server', 'overwatch-server' ]:
        mounts.append(
            docker.types.Mount(
                '/data-dir',
                os.path.join( root_volume_directory, 'input-server', 'data-dir' ),
                type = 'bind'
            )
        )
    else:
        mounts.append(
            docker.types.Mount(
                '/data-dir',
                os.path.join( root_volume_directory, dependency, 'data-dir' ),
                type = 'bind'
            )
        )


    mounts.append(
        docker.types.Mount(mount_path, volume_path, read_only=True, type='bind')
    )

    return mounts

def cleanup(client, dependencies, config):
    all_containers = {}
    for container in client.containers.list(all=True):
        all_containers[container.name] = container

    for dependency in dependencies:
        if dependency in list(all_containers.keys()):
            print(f"Cleaning up {dependency}")
            container = all_containers[dependency]
            container.stop()
            container.wait()
            mounts = container.attrs['Mounts']
            for mount in mounts:
                if mount['Destination'] == '/root/.dcp':
                    continue
                if os.path.exists(mount['Source']) and os.path.isdir(mount['Source']):
                    shutil.rmtree(mount['Source'])
                elif os.path.exists(mount['Source']):
                    os.remove(mount['Source'])
            container.remove()
            print(f"Done cleaning up {dependency}")
    print("Finished cleaning up all dependencies")
    return


def satisfy_needs(client, dependencies, config, keystores):
    
    assert os.path.exists(keystores), f"Given keystore path does not exist: {keystores}"

    all_containers = {}
    for container in client.containers.list(all=True):
        all_containers[container.name] = container

    root_volume_directory, volume_mounts = prep_directory(dependencies)

    for dependency in dependencies:
        if dependency in list(all_containers.keys()):
            print(f"Stopping {dependency}")
            container = all_containers[dependency]
            container.stop()
            container.wait()
            container.remove()
            print(f"Stopped and removed {dependency}")

        assert dependency in config.keys(), f"No config entry for {dependency}"

        dependency_config = config[dependency]
        
        mounts = make_mount_list( 
            dependency, 
            dependency_config, 
            root_volume_directory,
        )

        if dependency in 'overwatch-server':
            mounts.append(
                docker.types.Mount(
                    '/root/.dcp',
                    keystores,
                    type='bind',
                    read_only=True,
                )
            )

        pull_image( client, dependency_config['docker']['image'] )
        
        container = client.containers.create(
            dependency_config['docker']['image'],
            mounts = mounts,
            network_mode = 'host',
        )
        container.rename(dependency)
        container.start()
    print(f"Finished deploying dependencies: {dependencies}")




def setup_client():
    if hasattr(setup_client, "client"):
        return setup_client.client
    client = docker.from_env()
    pretty_client_info = json.dumps( client.version(), sort_keys=True, indent=2 )
    print(f"Connected to docker: \n{pretty_client_info}")
    setup_client.client = client
    return client


def _load_config(path):
    assert os.path.exists(path), f"Config provided does not exist: {path}"
    with open(path, 'r') as f:
        data = ''.join( f.readlines() )
    config = yaml.load(data, Loader=Loader)
    return config

def load_config(path):
    template_config = _load_config( os.path.join( os.path.dirname( __file__ ), 'template.config.yaml' ) )
    config = _load_config( path )

    out_config = copy.deepcopy( template_config )
    out_config = dictionary_update( out_config, config )

    return out_config



def write_config(path, data):
    with open(path, 'w') as f:
        f.write(
            yaml.dump( data, Dumper=Dumper )
        )
    return


def needs_cli(args = None):
    import argparse
    parser = argparse.ArgumentParser(description="A dependency satisfaction tool for overwatch using docker/python to simplify your CI setups!")
    parser.add_argument("dependencies", nargs="+", help="Dependencies to satisfy, must be any of 'overwatch-server', 'model-registry', 'input-server'")
    parser.add_argument("-c", "--config", type=str, help="Path to config.yaml for Overwatch CI Helper")
    parser.add_argument("--cleanup", action="store_true", help="Clean up all containers and remove from docker instance")
    parser.add_argument("--keystores", type=str, default="~/.dcp", help="Directory containing dcp keystores on host. Defaults to ~/.dcp")

    args = parser.parse_args(args)
    client = setup_client()
    config = load_config(args.config)

    print(json.dumps( config, sort_keys=True, indent=2 ))
    
    if args.cleanup:
        cleanup(client, args.dependencies, config)
    else:
        satisfy_needs(client, args.dependencies, config, os.path.expanduser(args.keystores))
