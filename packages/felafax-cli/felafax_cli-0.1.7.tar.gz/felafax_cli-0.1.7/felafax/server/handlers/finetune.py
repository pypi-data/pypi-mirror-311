from ...core.storage.base import StorageProvider
from typing import Dict, List, Tuple, AsyncGenerator
from ..models.finetune import FineTuneStoragePaths
from ..handlers.base import ListMetadataHandler
from ..models.finetune import FinetuneMetadata, FinetuneStatus, FineTuneRequest
from ..handlers.accelerator import AcceleratorHandler
from ..models.dataset import DatasetStoragePaths
from ..models.accelerator import AcceleratorRequest
from ..handlers.dataset import DatasetHandler
from datetime import datetime
import uuid
import yaml
from pathlib import Path
import asyncio
from ..models.finetune import DataConfig, TrainerConfig, CheckpointerConfig, InternalConfig, FineTuneConfig
from ..models.model import ModelMetadata, ModelPaths
from felafax.config import Config
from logging import getLogger

logger = getLogger(__name__)


class FineTuneHandler:
    # Model-specific configurations
    MODEL_CONFIGS = {
        "llama3": {
            "8b": {
                "provider": "tpu",
                "config": {
                    "accelerator_type": "v3",
                    "accelerator_core_count": 8,
                    "zone": "us-central1-a",
                }
            },
            "70b": {
                "provider": "tpu",
                "config": {
                    "accelerator_type": "v5p",
                    "accelerator_core_count": 8,
                    "zone": "us-east5-a",
                }
            },
            "405b": {
                "provider": "tpu",
                "config": {
                    "accelerator_type": "v5p",
                    "accelerator_core_count": 32,
                    "zone": "us-east5-a",
                }
            }
        }
    }

    DEFAULT_PATHS = {
        "trainer_dir": "/mnt/persistent-disk/train",
        "export_dir": "/mnt/persistent-disk/train/hf_export",
    }

    def __init__(self, storage_provider: StorageProvider, user_id: str):
        self._metadata_handler = ListMetadataHandler(FinetuneMetadata, FineTuneStoragePaths.metadata_path(user_id), "tune_id", storage_provider)
        self._accelerator_handler = AcceleratorHandler(storage_provider, user_id)
        self._dataset_handler = DatasetHandler(storage_provider, user_id)
        self._model_metadata_handler = ListMetadataHandler(ModelMetadata, ModelPaths.metadata_path(user_id), "model_id", storage_provider)

        self.storage = storage_provider
        self.user_id = user_id

    async def get_tune_info(self, tune_id: str) -> Dict:
        """Get tune metadata"""
        if not await self.check_finetune_job_exists(tune_id):
            logger.error(f"Tune {tune_id} not found")
            raise ValueError("Tune not found")
        path = FineTuneStoragePaths.status_path(self.user_id, tune_id)
        logger.debug(f"Getting tune info from {path}")
        return FinetuneStatus(**await self.storage.read_json(path))

    async def update_tune_info(self, tune_id: str, info: Dict) -> None:
        """Update tune metadata"""
        path = FineTuneStoragePaths.status_path(self.user_id, tune_id)
        await self.storage.write_json(path, info)

    async def get_tune_config(self, tune_id: str) -> Dict:
        """Get tune configuration"""
        path = FineTuneStoragePaths.user_config_path(self.user_id, tune_id)
        return await self.storage.read_yaml(path)

    async def update_tune_config(self, tune_id: str, config: Dict) -> None:
        """Update tune configuration"""
        path = FineTuneStoragePaths.user_config_path(self.user_id, tune_id)
        await self.storage.write_yaml(path, config)

    async def validate_dataset(self, dataset_id: str) -> bool:
        return await self._dataset_handler.validate_dataset(dataset_id)
    
    async def check_finetune_job_exists(self, tune_id: str) -> bool:
        tune = await self._metadata_handler.get(tune_id)
        return tune is not None
    
    async def get_all_finetune_jobs(self) -> List[FinetuneMetadata]:
        return await self._metadata_handler.list()

    def _generate_trainer_config(self, request_config: Dict, model_name: str, tune_id: str) -> Tuple[Dict, Dict]:
        """Generate complete configuration by combining request config with defaults"""
        # Get model-specific accelerator config
        model_config = self._get_model_config(model_name)
        
        # Prepare trainer config
        trainer_config = request_config.get("trainer_config", {})
        # TODO: map from model_name to hf_repo
        # trainer_config["model_name"] = "meta-llama/Llama-3.2-1B-Instruct" # model_name

        # Map model names to Hugging Face repos
        model_map = {
            "llama3_2-1b": "meta-llama/Llama-3.2-1B-Instruct",
            "llama3_1-8b": "meta-llama/Llama-3.1-8B-Instruct",
            "llama3_1-70b": "meta-llama/Llama-3.1-70B-Instruct",
            "llama3_1-405b": "meta-llama/Llama-3.1-405B-Instruct"
        }
        trainer_config["model_name"] = model_map.get(model_name.lower(), model_name)

        # Create full config using Pydantic model
        trainer_config = FineTuneConfig(
            trainer_dir=self.DEFAULT_PATHS["trainer_dir"],
            export_dir=self.DEFAULT_PATHS["export_dir"],
            hf_token=request_config.get("hf_token", ""),
            hf_repo=request_config.get("hf_repo", ""),
            test_mode=True,
            data_config=DataConfig(**(request_config.get("data_config", {}))),
            trainer_config=TrainerConfig(**trainer_config),
            checkpointer_config=CheckpointerConfig(**(request_config.get("checkpointer_config", {})))
        )

        # Create internal config
        internal_config = InternalConfig(
            user_id=self.user_id,
            tune_id=tune_id,
            base_storage_path="/mnt/persistent-disk",
            trainer_dir=self.DEFAULT_PATHS["trainer_dir"],
            export_dir=self.DEFAULT_PATHS["export_dir"],
            dataset_path="/mnt/persistent-disk/dataset.jsonl",
            model_gcs_path="",  # Will be set later
            dataset_gcs_path=""  # Will be set later
        )

        return trainer_config.dict(), internal_config.dict()

    async def _create_model_for_tune(self, tune_id: str, request: FineTuneRequest) -> ModelMetadata:
        """Create a new model entry for this fine-tuning job"""
        model_id = f"model_{uuid.uuid4().hex[:12]}"
        current_time = datetime.utcnow()
        
        model = ModelMetadata(
            model_id=model_id,
            base_model=request.model_name,
            created_at=current_time,
            updated_at=current_time,
            status="training",
            description=f"Fine-tuned from {request.model_name}",
            config={
                "tune_id": tune_id,
                "dataset_id": request.dataset_id,
                "training_config": request.config
            }
        )
        
        # Save model metadata
        await self._model_metadata_handler.add(model)
        
        return model

    async def start_finetune(self, request: FineTuneRequest) -> Tuple[str, str, str]:
        """Start a new fine-tuning job"""
        tune_id = f"tune_{uuid.uuid4().hex[:12]}"
        logger.info(f"Starting new fine-tune job {tune_id} for model {request.model_name}")
        
        try:
            # Create new model first
            model = await self._create_model_for_tune(tune_id, request)
            logger.debug(f"Created model {model.model_id} for tune {tune_id}")
            
            # Create status object
            status = FinetuneStatus(
                tune_id=tune_id,
                status="initializing",
                progress=0,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            # Save status
            await self.update_tune_info(tune_id, status.dict())

            # Generate full configuration and internal config
            trainer_config, internal_config = self._generate_trainer_config(request.config, request.model_name, tune_id)
            
            # Add model GCS path to internal config
            internal_config["model_gcs_path"] = ModelPaths.full_model_path(self.user_id, model.model_id)
            
            # Add dataset GCS path to internal config
            dataset_metadata = await self._dataset_handler.get_dataset(request.dataset_id)
            internal_config["dataset_gcs_path"] = dataset_metadata.full_file_path
            # this is the path to the dataset on the local machine for copying
            internal_config["dataset_path"] = f"{internal_config['base_storage_path']}/{dataset_metadata.file_name}"
            # set the dataset path for trainer
            trainer_config["data_config"]["data_source"] = internal_config["dataset_path"]
            
            # Create temporary files for configs
            trainer_config_path = Path("/tmp") / "trainer_config.yml"
            internal_config_path = Path("/tmp") / "internal_config.yml"
            config_path = Path("/tmp") / "config.yml"

            try:
                # Write all config files
                with open(trainer_config_path, "w") as f:
                    yaml.dump(trainer_config, f)
                
                with open(internal_config_path, "w") as f:
                    yaml.dump(internal_config, f)
                    
                with open(config_path, "w") as f:
                    yaml.dump(request.config, f)
                    
                # Upload all configs
                await asyncio.gather(
                    self.storage.upload_file(
                        config_path,
                        FineTuneStoragePaths.user_config_path(self.user_id, tune_id)
                    ),
                    self.storage.upload_file(
                        trainer_config_path,
                        FineTuneStoragePaths.trainer_config_path(self.user_id, tune_id)
                    ),
                    self.storage.upload_file(
                        internal_config_path,
                        FineTuneStoragePaths.internal_config_path(self.user_id, tune_id)
                    )
                )
            finally:
                # Cleanup temporary files
                for path in [config_path, trainer_config_path, internal_config_path]:
                    if path.exists():
                        path.unlink()

            acclerator_config = self._get_model_config(request.model_name)
            
            docker_image = Config.FINETUNE_IMAGE_NAME
            docker_env = {
                "GCS_JOB_PATH": FineTuneStoragePaths.tune_path(self.user_id, tune_id, include_bucket=True),
                "SCRIPT_NAME": "execute_trainer.py"
            }
            
            # Create AcceleratorRequest from model config
            accelerator_request = AcceleratorRequest(
                type=acclerator_config["provider"],
                accelerator_type=acclerator_config["config"]["accelerator_type"],
                accelerator_core_count=acclerator_config["config"]["accelerator_core_count"],
                zone=acclerator_config["config"]["zone"],
                framework="jax",
                attach_disk=True,  
                disk_size_gb=1000,
                docker_image=docker_image,
                docker_env=docker_env,
                tags=["allow-ssh-tpu-vm"],
                **request.config.get("accelerator", {})
            )

            accelerator = await self._accelerator_handler.create_accelerator(
                request=accelerator_request,
            )

            # Create new tune metadata
            new_tune = FinetuneMetadata(
                tune_id=tune_id,
                model_id=model.model_id,
                dataset_id=request.dataset_id,
                base_model=request.model_name,
                status="running",
                accelerator_id=accelerator.accelerator_id,
                created_at=status.created_at,
                updated_at=status.updated_at
            )
            
            # Add to catalog
            await self._metadata_handler.add(new_tune)

            logger.info(f"Successfully started fine-tune job {tune_id}")
            return tune_id, "initializing", "Fine-tuning job created successfully"
        except Exception as e:
            logger.error(f"Failed to start fine-tune job {tune_id}: {str(e)}")
            raise

    async def stop_finetune(self, tune_id: str) -> Tuple[str, str, str]:
        """Stop a fine-tuning job"""
        logger.info(f"Stopping fine-tune job {tune_id}")
        
        # Get tune metadata
        tune = await self._metadata_handler.get(tune_id)
        if not tune:
            logger.error(f"Tune {tune_id} not found")
            raise ValueError("Tune not found")

        current_time = datetime.utcnow()
        new_status = "stopping"

        # Stop accelerator if one exists
        if tune.accelerator_id:
            asyncio.create_task(
                self._accelerator_handler.stop_accelerator(tune.accelerator_id)
            )

        # Update both status and metadata concurrently
        async def update_status():
            status = await self.get_tune_info(tune_id)
            status.status = new_status
            status.updated_at = current_time
            await self.update_tune_info(tune_id, status.dict())

        async def update_metadata():
            tune.status = new_status
            tune.updated_at = current_time
            await self._metadata_handler.update(tune)

        try:
            await asyncio.gather(update_status(), update_metadata())
            logger.info(f"Successfully stopped fine-tune job {tune_id}")
            return tune_id, new_status, "Stop signal sent to fine-tuning job"
        except Exception as e:
            logger.error(f"Failed to stop fine-tune job {tune_id}: {str(e)}")
            raise
    
    def _get_model_family(self, model_name: str) -> str:
        return model_name.split("-")[0].lower()

    def _get_model_size(self, model_name: str) -> str:
        return model_name.split("-")[1]

    def _get_model_config(self, model_name: str) -> Dict:
        model_family = self._get_model_family(model_name)
        model_size = self._get_model_size(model_name)
        return self.MODEL_CONFIGS.get(model_family, {}).get(model_size, {})

    async def stream_logs(self, tune_id: str, start_byte: int = 0) -> AsyncGenerator[str, None]:
        """Stream debug logs for a fine-tuning job"""
        log_path = FineTuneStoragePaths.stdout_path(self.user_id, tune_id)
        
        try:
            # Stream content as text starting from start_byte
            async for chunk in self.storage.stream_file_text(log_path, start_position=start_byte):
                yield chunk
        except Exception as e:
            logger.error(f"Error streaming logs for tune {tune_id}: {str(e)}")
            yield f"Error reading logs: {str(e)}\n"
        
    async def get_log_file_size(self, tune_id: str) -> int:
        """Get the size of the log file"""
        log_path = FineTuneStoragePaths.stdout_path(self.user_id, tune_id)
        return await self.storage.get_file_size(log_path)

