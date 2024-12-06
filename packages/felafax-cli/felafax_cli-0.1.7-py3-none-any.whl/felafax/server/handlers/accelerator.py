from typing import Dict, Any, Optional, List
import uuid
import asyncio
from datetime import datetime
from ...config import Config
from ...core.accelerators.base import AcceleratorProvider, AcceleratorStatus
from ...core.accelerators.tpu import TPUProvider
from ...core.storage.base import StorageProvider
from ..models.accelerator import AcceleratorMetadata, AcceleratorStoragePaths, AcceleratorRequest
from ..handlers.base import ListMetadataHandler
from ..common import generate_vm_name
from dataclasses import dataclass
from felafax.core.accelerators.tpu import TPUConfig
import logging

logger = logging.getLogger(__name__)

@dataclass
class AcceleratorSpec:
    provider: str
    config: Dict[str, Any]
    docker_config: Optional[Dict[str, Any]] = None

class AcceleratorHandler:
    def __init__(self, storage_provider: StorageProvider, user_id: str):
        logger.info(f"Initializing AcceleratorHandler for user {user_id}")
        self.storage_provider = storage_provider
        self.user_id = user_id
        self._provider_map = {
            "tpu": TPUProvider
        }
        self._metadata_handler = ListMetadataHandler(
            AcceleratorMetadata, 
            AcceleratorStoragePaths.metadata_path(self.user_id), 
            "accelerator_id", 
            self.storage_provider
        )

    async def create_accelerator(
        self,
        request: AcceleratorRequest,
        wait_for_ready: bool = False
    ) -> AcceleratorMetadata:
        """Create and start a new accelerator
        
        Args:
            request: Accelerator configuration request
            tags: Optional list of tags
            wait_for_ready: Whether to wait for accelerator to be ready
        """
        logger.info(f"Creating accelerator with type {request.type}")
        # Generate IDs
        accelerator_id = f"acc_{uuid.uuid4().hex[:8]}"
        vm_name = generate_vm_name()

        # Build provider config based on request
        if request.type == "tpu":
            # Map framework to runtime version
            runtime_version = {
                "jax": "tpu-vm-tf-2.16.1-pod-pjrt",
                "pytorch-xla": "tpu-vm-pt-2.0",
            }.get(request.framework, "tpu-vm-tf-2.16.1-pod-pjrt")

            full_config = TPUConfig(
                project_id=Config.GCS_PROJECT_ID,
                name=vm_name,
                accelerator_type=request.accelerator_type,
                accelerator_core_count=request.accelerator_core_count,
                runtime_version=runtime_version,
                attach_disk=request.attach_disk,
                disk_size_gb=request.disk_size_gb,
                docker_image=request.docker_image,
                docker_env=request.docker_env or {},
                ssh_key=request.ssh_key,
                zone=request.zone,
                tags=tags or [],
                preemptible=request.preemptible,
                custom_config=request.custom_config or {},
            )
        else:
            raise ValueError(f"Unsupported provider type: {request.type}")

        # Create provider instance
        provider_class = self._provider_map.get(request.type)
        if not provider_class:
            raise ValueError(f"Unsupported provider type: {request.type}")
        
        logger.debug(f"Initializing provider {request.type} with config: {full_config}")
        provider_instance = provider_class()
        await provider_instance.initialize(full_config.to_dict())
        
        # Create metadata
        current_time = datetime.utcnow()
        metadata = AcceleratorMetadata(
            accelerator_id=accelerator_id,
            name=vm_name,
            provider=request.type,
            created_at=current_time,
            updated_at=current_time,
            status=AcceleratorStatus.PROVISIONING,
            config=full_config.to_dict(),
            tags=tags or []
        )

        # Save catalog entry
        await self._metadata_handler.add(metadata)

        async def start_and_update():
            try:
                logger.info(f"Starting accelerator {accelerator_id}")
                response = await provider_instance.start()
                logger.debug(f"Accelerator started successfully: {response}")
                metadata.status = AcceleratorStatus.READY
                metadata.config["zone"] = response["zone"]
                metadata.ip_address = response["ip_address"]
                await self._metadata_handler.update(metadata)
            except Exception as e:
                logger.error(f"Failed to start accelerator {accelerator_id}: {str(e)}")
                metadata.status = AcceleratorStatus.ERROR
                await self._metadata_handler.update(metadata)
                raise e

        if wait_for_ready:
            await start_and_update()
        else:
            asyncio.create_task(start_and_update())

        return metadata
    async def stop_accelerator(self, accelerator_id: str) -> None:
        """Stop and cleanup an accelerator"""
        logger.info(f"Stopping accelerator {accelerator_id}")
        # Get accelerator metadata
        metadata = await self._metadata_handler.get(accelerator_id)
        if not metadata:
            raise ValueError(f"Accelerator {accelerator_id} not found")
        
        # Initialize provider
        provider_class = self._provider_map.get(metadata.provider)
        if not provider_class:
            raise ValueError(f"Unsupported provider: {metadata.provider}")
            
        try:
            provider = provider_class()
            await provider.initialize(metadata.config)
            asyncio.create_task(provider.stop())
            logger.debug(f"Stop task created for accelerator {accelerator_id}")
        except Exception as e:
            logger.error(f"Error stopping accelerator {accelerator_id}: {str(e)}")
            raise

        # Update metadata
        metadata.status = AcceleratorStatus.TERMINATED
        metadata.updated_at = datetime.utcnow()
        await self._metadata_handler.update(metadata)
    
    async def get_ip_address(self, accelerator_id: str) -> str:
        """Get the IP address of an accelerator"""
        logger.debug(f"Getting IP address for accelerator {accelerator_id}")
        metadata = await self._metadata_handler.get(accelerator_id)
        if metadata.ip_address is None:
            logger.info(f"IP address not cached, fetching from provider for {accelerator_id}")
            # let's use the provider to get the IP address
            provider_class = self._provider_map.get(metadata.provider)
            if not provider_class:
                raise ValueError(f"Unsupported provider: {metadata.provider}")
            
            provider = provider_class()
            await provider.initialize(metadata.config)
            metadata.ip_address = await provider.get_ip_address()
            await self._metadata_handler.update(metadata)

        return metadata.ip_address

