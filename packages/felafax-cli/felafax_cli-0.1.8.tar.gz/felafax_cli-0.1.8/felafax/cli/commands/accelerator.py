import typer
from datetime import datetime
from typing import Optional
import httpx
from ..common import get_user_id, require_auth, get_server_uri
import logging

logger = logging.getLogger(__name__)

accelerator_app = typer.Typer(help="Accelerator management commands")

SUPPORTED_ACCELERATOR_TYPES = ["tpu"]
SUPPORTED_FRAMEWORKS = ["jax", "pytorch-xla"]
SUPPORTED_MACHINE_TYPES = ["v3", "v5p"]
SUPPORTED_MACHINE_CORES = [8, 16, 32]
AUTO_SHUTDOWN_HOURS = [1, 2, 3, 4, 5, 6]

# write a function to validate all typer options for start_accelerator
def validate_args(args):
    if args["type"] not in SUPPORTED_ACCELERATOR_TYPES:
        msg = f"Invalid accelerator type: {args['type']}. Must be one of: {', '.join(SUPPORTED_ACCELERATOR_TYPES)}"
        logger.error(msg)
        raise typer.Abort(msg)
    if args["accelerator_type"] not in SUPPORTED_MACHINE_TYPES:
        msg = f"Invalid machine type: {args['accelerator_type']}. Must be one of: {', '.join(SUPPORTED_MACHINE_TYPES)}"
        logger.error(msg)
        raise typer.Abort(msg)
    if args["accelerator_core_count"] not in SUPPORTED_MACHINE_CORES:
        msg = f"Invalid machine cores: {args['accelerator_core_count']}. Must be one of: {', '.join(map(str, SUPPORTED_MACHINE_CORES))}"
        logger.error(msg)
        raise typer.Abort(msg)
    if args["framework"] not in SUPPORTED_FRAMEWORKS:
        msg = f"Invalid framework: {args['framework']}. Must be one of: {', '.join(SUPPORTED_FRAMEWORKS)}"
        logger.error(msg)
        raise typer.Abort(msg)
    if args["auto_shutdown"] not in AUTO_SHUTDOWN_HOURS:
        msg = f"Invalid auto-shutdown time: {args['auto_shutdown']}. Must be one of: {', '.join(map(str, AUTO_SHUTDOWN_HOURS))}"
        logger.error(msg)
        raise typer.Abort(msg)

@accelerator_app.command("start")
@require_auth
def start_accelerator(
    type: str = typer.Option("tpu", help=f"Accelerator type (tpu)"),
    accelerator_type: str = typer.Option("v3", help=f"Accelerator type (v3, v5p)"),
    accelerator_core_count: int = typer.Option(8, help="Number of cores (8, 16, 32)", min=8, max=32),
    framework: str = typer.Option("jax", help="Framework to use (jax, pytorch-xla)"),
    disk_size: int = typer.Option(1000, help="Disk size in GB (if disk is enabled)"),
    attach_disk: bool = typer.Option(True, help="Whether to attach persistent disk"),
    auto_shutdown: int = typer.Option(3, help="Auto-shutdown time in hours (1-6)", min=1, max=6),
    env_vars: Optional[str] = typer.Option(None, help="Environment variables in KEY1=VAL1,KEY2=VAL2 format"),
    ssh_key_path: Optional[str] = typer.Option(None, help="Path to SSH public keys file"),
    wait: bool = typer.Option(False, help="Wait for accelerator to be ready")
):
    """Start a new TPU accelerator instance"""
    validate_args(locals())
    
    # Parse environment variables
    docker_env = {}
    if env_vars:
        try:
            for pair in env_vars.split(','):
                key, value = pair.split('=')
                docker_env[key.strip()] = value.strip()
        except ValueError:
            logger.error("Invalid environment variables format. Use KEY1=VAL1,KEY2=VAL2")
            raise typer.Abort()

    # Read SSH key if provided
    ssh_key = None
    if ssh_key_path:
        try:
            with open(ssh_key_path, 'r') as f:
                ssh_key = f.read().strip()
        except Exception as e:
            logger.error(f"Failed to read SSH key file: {e}")
            raise typer.Abort()

    # Prepare request payload
    payload = {
        "type": type,
        "accelerator_type": accelerator_type,
        "accelerator_core_count": accelerator_core_count,
        "framework": framework,
        "attach_disk": attach_disk,
        "disk_size_gb": disk_size if attach_disk else None,
        "auto_shutdown": auto_shutdown,
        "docker_env": docker_env if docker_env else None,
        "ssh_key": ssh_key,
        "wait": wait
    }

    try:
        user_id = get_user_id()
        url = f"{get_server_uri()}/accelerators/{user_id}/start"
        
        timeout = 600.0 if wait else 30.0  # 10 mins if waiting, 30s otherwise
        if wait:
            logger.info(f"Waiting for accelerator to be ready. This will take 5-10 minutes...")

        with httpx.Client(timeout=timeout) as client:
            response = client.post(url, json=payload)
            response.raise_for_status()
            
            result = response.json()
            typer.echo(f"Successfully started accelerator: {result['accelerator_id']}")
            typer.echo(f"Status: {result['status']}")
    except httpx.HTTPError as e:
        logger.error(f"Failed to start accelerator: {e}")
        raise typer.Abort()

@accelerator_app.command("stop")
@require_auth
def stop_accelerator(
    accelerator_id: str = typer.Option(..., help="Accelerator ID to stop")
):
    """Stop a running accelerator"""
    pass

@accelerator_app.command("list")
@require_auth
def list_accelerators():
    """List all accelerators"""
    try:
        user_id = get_user_id()
        url = f"{get_server_uri()}/accelerators/{user_id}/list"
        
        with httpx.Client() as client:
            response = client.get(url)
            response.raise_for_status()
            
            accelerators = response.json()
            if not accelerators:
                typer.echo("No accelerators found")
                return
                
            for acc in accelerators:
                typer.echo(f"ID: {acc['accelerator_id']}")
                typer.echo(f"Name: {acc['name']}")
                typer.echo(f"Status: {acc['status']}")
                typer.echo(f"Type: {acc['provider']}")
                typer.echo(f"Created: {acc['created_at']}")
                typer.echo("---")
                
    except httpx.HTTPError as e:
        logger.error(f"Failed to list accelerators: {e}")
        raise typer.Abort()

@accelerator_app.command("status")
@require_auth
def get_status(
    accelerator_id: str = typer.Option(..., help="Accelerator ID to check status for")
):
    """Get status of a specific accelerator"""
    try:
        user_id = get_user_id()
        url = f"{get_server_uri()}/accelerators/{user_id}/{accelerator_id}/status"
        
        with httpx.Client() as client:
            response = client.get(url)
            response.raise_for_status()
            
            accelerator = response.json()
            typer.echo(f"ID: {accelerator['accelerator_id']}")
            typer.echo(f"Name: {accelerator['name']}")
            typer.echo(f"Status: {accelerator['status']}")
            typer.echo(f"Type: {accelerator['provider']}")
            typer.echo(f"Created: {accelerator['created_at']}")
            
    except httpx.HTTPError as e:
        logger.error(f"Failed to get accelerator status: {e}")
        raise typer.Abort()

@accelerator_app.command("delete")
@require_auth
def delete_accelerator(
    accelerator_id: str = typer.Option(None, "--accelerator-id", "-id", help="Accelerator ID to delete"),
    all: bool = typer.Option(False, help="Delete all accelerators")
):
    """Delete an accelerator and its resources"""
    try:
        user_id = get_user_id()
        
        if all:
            # Get list of all accelerators first
            list_url = f"{get_server_uri()}/accelerators/{user_id}/list"
            with httpx.Client() as client:
                response = client.get(list_url)
                response.raise_for_status()
                accelerators = response.json()
                
                if not accelerators:
                    typer.echo("No accelerators found to delete")
                    return
                    
                for acc in accelerators:
                    acc_id = acc['accelerator_id']
                    delete_url = f"{get_server_uri()}/accelerators/{user_id}/{acc_id}"
                    response = client.delete(delete_url)
                    response.raise_for_status()
                    typer.echo(f"Deleted accelerator {acc_id}")
                    
                typer.echo("Successfully deleted all accelerators")
                return
                
        if not accelerator_id:
            typer.echo("Must specify either --accelerator-id or --all")
            raise typer.Abort()
            
        url = f"{get_server_uri()}/accelerators/{user_id}/{accelerator_id}"
        with httpx.Client() as client:
            response = client.delete(url)
            response.raise_for_status()
            
            result = response.json()
            typer.echo(result["message"])
            
    except httpx.HTTPError as e:
        logger.error(f"Failed to delete accelerator: {e}")
        raise typer.Abort()