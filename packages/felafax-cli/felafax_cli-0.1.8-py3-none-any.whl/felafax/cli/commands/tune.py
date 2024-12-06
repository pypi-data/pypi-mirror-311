import typer
from datetime import datetime
import yaml
from ..common import get_user_id, require_auth, get_server_uri
import httpx
from pathlib import Path
from ...core.constants import SUPPORTED_MODELS
import sys
from time import sleep

tune_app = typer.Typer(help="Tuning commands")

@tune_app.command("init-config")
def init_config():
    """Initialize a new fine-tuning configuration file"""
    
    config = {
        'data_config': {
            'batch_size': 16,
            'max_seq_length': 2048
        },
        'trainer_config': {
            'param_dtype': 'bfloat16',
            'compute_dtype': 'bfloat16', 
            'num_epochs': 1,
            'num_steps': 5,
            'learning_rate': 1e-3,
            'lora_rank': 16,
            'use_lora': True,
            'log_interval': 5,
            'eval_interval': 5,
            'eval_steps': 10
        },
        'huggingface_config': {
            'hf_repo': '',  
            'hf_token': ''  
        }
    }
    
    # Generate filename with date prefix
    date_suffix = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    filename = f"felafax-finetune-{date_suffix}.yml"
    
    with open(filename, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    typer.echo(f"Created fine-tuning configuration file: {filename}") 

@tune_app.command("start")
@require_auth
def start_tuning(
    model: str = typer.Option(..., "--model", "-m", help=f"Base model to fine-tune (one of: {', '.join(SUPPORTED_MODELS)})"),
    config: str = typer.Option(..., "--config", "-c", help="Path to config YAML file"), 
    dataset_id: str = typer.Option(..., "--dataset-id", "-d", help="Dataset ID to use for training")
):
    """Start a new fine-tuning job"""
    # Validate model
    if model not in SUPPORTED_MODELS:
        typer.echo(f"Error: Invalid model. Must be one of: {', '.join(SUPPORTED_MODELS)}")
        raise typer.Exit(1)
        
    # Load and validate config file
    try:
        config_path = Path(config)
        if not config_path.exists():
            typer.echo(f"Error: Config file not found: {config}")
            raise typer.Exit(1)
            
        with open(config_path) as f:
            config_data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        typer.echo(f"Error: Invalid YAML config file: {e}")
        raise typer.Exit(1)

    # Prepare request payload
    request_data = {
        "model_name": model,
        "dataset_id": dataset_id,
        "config": config_data
    }

    user_id = get_user_id()
    
    # Make API request
    try:
        server_uri = get_server_uri()
        response = httpx.post(
            f"{server_uri}/fine-tune/{user_id}/start",
            json=request_data
        )
        
        if response.status_code == 200:
            result = response.json()
            typer.echo(f"Started fine-tuning job: {result['tune_id']}")
            typer.echo(f"Status: {result['status']}")
            typer.echo(f"Message: {result['message']}")
        else:
            typer.echo(f"Error: {response.status_code} - {response.text}")
            raise typer.Exit(1)
            
    except httpx.RequestError as e:
        typer.echo(f"Error connecting to API: {e}")
        raise typer.Exit(1)
@tune_app.command("list")
def list_jobs():
    """List all fine-tuning jobs"""
    user_id = get_user_id()
    server_uri = get_server_uri()
    
    try:
        response = httpx.get(f"{server_uri}/fine-tune/{user_id}/list")
        response.raise_for_status()
        jobs = response.json()
        
        # Print header
        typer.echo("\nFine-tuning Jobs:")
        typer.echo("-" * 80)
        typer.echo(f"{'ID':12} | {'Model Name':20} | {'Status':10} | {'Created At'}")
        typer.echo("-" * 80)
        
        # Print each job
        for job in jobs:
            created_at = job['created_at'].split('T')[0]  # Just get the date part
            typer.echo(f"{job['tune_id']:12} | {job['base_model']:20} | {job['status']:10} | {created_at}")
            
    except httpx.RequestError as e:
        typer.echo(f"Error connecting to API: {e}")
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"Error: {str(e)}")
        raise typer.Exit(1)

@tune_app.command("status")
@require_auth
def get_status(
    job_id: str = typer.Option(..., help="Job ID to check status for")
):
    """Get status of a specific fine-tuning job"""
    user_id = get_user_id()
    server_uri = get_server_uri()
    
    try:
        response = httpx.get(f"{server_uri}/fine-tune/{user_id}/{job_id}/status")
        response.raise_for_status()
        status = response.json()
        
        # Print status information
        typer.echo("\nFine-tuning Job Status:")
        typer.echo("-" * 40)
        typer.echo(f"Job ID: {status['tune_id']}")
        typer.echo(f"Status: {status['status']}")
        typer.echo(f"Created: {status['created_at']}")
        typer.echo(f"Last Updated: {status['updated_at']}")
        if status.get('progress') is not None:
            typer.echo(f"Progress: {status['progress']:.1%}")
            
    except httpx.RequestError as e:
        typer.echo(f"Error connecting to API: {e}")
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"Error: {str(e)}")
        raise typer.Exit(1)

@tune_app.command("stop")
@require_auth
def stop_job(
    job_id: str = typer.Option(..., help="Job ID to stop")
):
    """Stop a running fine-tuning job"""
    user_id = get_user_id()
    server_uri = get_server_uri()
    
    try:
        response = httpx.post(f"{server_uri}/fine-tune/{user_id}/{job_id}/stop")
        response.raise_for_status()
        result = response.json()
        
        typer.echo(f"Stopped fine-tuning job: {result['tune_id']}")
        typer.echo(f"Status: {result['status']}")
        typer.echo(f"Message: {result['message']}")
            
    except httpx.RequestError as e:
        typer.echo(f"Error connecting to API: {e}")
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"Error: {str(e)}")
        raise typer.Exit(1)


@tune_app.command("debug", hidden=True)
@require_auth
def stream_logs(
    job_id: str = typer.Option(..., help="Job ID to stream logs for"),
    follow: bool = typer.Option(False, "--follow", "-f", help="Follow log output"),
):
    """Stream logs from a fine-tuning job"""
    user_id = get_user_id()
    server_uri = get_server_uri()
    
    try:
        last_size = 0
        first_read = True
        
        while True:
            # Only use range header after first read
            headers = {'Range': f'bytes={last_size}-'} if not first_read else {}
            
            with httpx.stream('GET', f"{server_uri}/fine-tune/{user_id}/{job_id}/log", headers=headers) as response:
                # Handle 416 (Range Not Satisfiable) for follow mode
                if response.status_code == 416:
                    if not follow:
                        break
                    sleep(1)
                    continue
                    
                response.raise_for_status()
                
                # Stream the content
                for chunk in response.iter_bytes():
                    if chunk:
                        sys.stdout.buffer.write(chunk)
                        sys.stdout.buffer.flush()
                        last_size += len(chunk)
            
            # Break if not following or after first read without follow
            if not follow and not first_read:
                break
                
            first_read = False
            sleep(1)
            
    except httpx.RequestError as e:
        typer.echo(f"Error connecting to API: {e}", err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(1) 