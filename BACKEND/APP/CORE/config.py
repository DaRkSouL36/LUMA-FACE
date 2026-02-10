import os
from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # API INFO
    PROJECT_NAME: str = "FACE ENHANCEMENT API"
    API_V1_STR: str = "/api/v1"
    
    # CORS CONFIGURATION
    # PARSES A COMMA-SEPARATED STRING INTO A LIST OF URLS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # MODEL & HARDWARE SETTINGS
    DEVICE: str = "cuda" if os.environ.get("CUDA_VISIBLE_DEVICES") else "cpu"
    GPU_ID: int = 0
    
    # MODEL PATHS
    GFPGAN_MODEL_PATH: str = "WEIGHTS/GFPGANv1.3.pth"
    REALESRGAN_MODEL_PATH: str = "WEIGHTS/RealESRGAN_x4plus.pth"
    INSIGHTFACE_MODEL_NAME: str = "antelopev2" # buffalo_l or antelopev2
    
    # PROCESSING LIMITS
    MAX_UPLOAD_SIZE_BYTES: int = 10 * 1024 * 1024  # 10 MB
    DEFAULT_UPSCALE_FACTOR: int = 2

    # ENV FILE CONFIG
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

# INSTANTIATE SETTINGS ONCE
settings = Settings()