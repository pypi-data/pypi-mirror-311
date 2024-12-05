import click
from nomad_media_pip.src.nomad_sdk import Nomad_SDK

import json
import os
from platformdirs import user_config_dir

# Set the configuration directory and path
CONFIG_DIR = user_config_dir("nomad_media_cli")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

@click.group()
@click.option("--config-path", default=CONFIG_PATH, help="Path to the configuration file")
@click.pass_context
def cli(ctx, config_path):
    """Nomad Media CLI"""
    ctx.ensure_object(dict)
    ctx.obj["config_path"] = config_path    

def initialize_sdk(ctx):
    config_path = ctx.obj["config_path"]    

    try:
        if os.path.exists(config_path):
            with open(config_path, "r") as file:
                config = json.load(file)
            ctx.obj["nomad_sdk"] = Nomad_SDK(config)
        else:
            ctx.obj["nomad_sdk"] = None
    
    except Exception as e:
        click.echo(f"Error loading configuration: {e}")
        ctx.obj["nomad_sdk"] = None

@cli.command()
@click.option("--username", required=True, help="Username for authentication")
@click.option("--password", required=True, help="Password for authentication")
@click.option("--service-api-url", required=True, help="API URL for the service")
@click.option("--api-type", default="admin", help="API type (i.e. admin, portal )")
@click.option("--debug-mode", is_flag=True, help="Enable debug mode")
@click.option("--singleton", is_flag=True, help="Enable singleton mode")
@click.pass_context
def init(ctx, username, password, service_api_url, api_type, debug_mode, singleton):
    """Initialize the SDK and save configuration"""
    
    config_path = ctx.obj["config_path"]
    config_dir = os.path.dirname(config_path)
    os.makedirs(config_dir, exist_ok=True)
    
    config = {
        "username": username,
        "password": password,
        "serviceApiUrl": service_api_url,
        "apiType": api_type,
        "debugMode": debug_mode,
        "singleton": singleton,
    }
    
    try:
        with open(config_path, "w") as file:
            json.dump(config, file, indent=4)
    
    except Exception as e:
        click.echo(f"Error saving configuration: {e}")
    
@cli.command()
@click.option("--id", help="Can be an assetId (file), an assetId (folder), a collectionId, a savedSearchId (lower priority).")
@click.option("--path", help="Is the objectKey (which defaults to the default content bucket) or the url to the folder.")
@click.pass_context
def list_assets(ctx, id, path):
    """List assets"""
    
    initialize_sdk(ctx)

    config_path = ctx.obj["config_path"]

    if not os.path.exists(config_path):
        click.echo("No configuration found. Please run 'init' first.")
        return
    
    try:
        filter = None
        if id: 
            filter = [{
                "fieldName": "uuid",
                "operator": "equals",
                "values": id
            }]
        elif path:
            if "::" not in path:
                click.echo("Please provide a valid path.")
                return

            filter = [{
                "fieldName": "url",
                "operator": "equals",
                "values": path
            }]
        else:
            click.echo("Please provide an id or path.")
            return

        nomad_sdk = ctx.obj["nomad_sdk"]
        results = nomad_sdk.search(None, None, None, filter, None, None, None, None, None, None, None, None, None, None, None)
        
        if (len(results["items"]) == 0):
            click.echo("No assets found.")
            return
        
        click.echo(json.dumps(results["items"], indent=4))
    
    except Exception as e:
        click.echo(f"Error listing assets: {e}")

if __name__ == '__main__':
    cli(obj={})

