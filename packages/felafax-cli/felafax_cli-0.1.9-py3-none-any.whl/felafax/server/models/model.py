from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, List
from felafax.config import Config

class ModelMetadata(BaseModel):
    """Model metadata schema"""
    model_id: str
    base_model: str
    created_at: datetime
    updated_at: datetime
    status: str  # e.g., "training", "ready", "failed"
    description: Optional[str] = None
    config: Dict = {}

class ModelPaths:
    """Model storage path generator"""
    
    @staticmethod
    def base_path(model_id: str) -> str:
        return f"models/{model_id}"
    
    @staticmethod
    def weights_path(model_id: str) -> str:
        return f"models/{model_id}/weights"
    
    @staticmethod
    def config_path(model_id: str) -> str:
        return f"models/{model_id}/config.json"
    
    @staticmethod
    def metadata_path(user_id: str) -> str:
        return f"users/{user_id}/metadata/models.json"
    
    @staticmethod
    def model_path(user_id: str, model_id: str) -> str:
        """Get the relative GCS path for a model"""
        return f"users/{user_id}/models/{model_id}"

    @staticmethod
    def full_model_path(user_id: str, model_id: str) -> str:
        """Get the full GCS path for a model including the bucket name"""
        return f"gs://{Config.GCS_BUCKET_NAME}/{ModelPaths.model_path(user_id, model_id)}"
    