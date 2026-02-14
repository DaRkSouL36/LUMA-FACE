import os
from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # =========================
    # APP SETTINGS
    # =========================
    PROJECT_NAME: str = "FACE ENHANCEMENT API"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True

    # =========================
    # CORS CONFIGURATION
    # PARSES COMMA-SEPARATED ORIGIN STRINGS INTO A LIST
    # =========================
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # =========================
    # HARDWARE SETTINGS
    # DEVICE CAN BE cpu OR cuda (SET VIA .env)
    # =========================
    DEVICE: str = os.environ.get("DEVICE", "cpu")
    GPU_ID: int = 0

    # =========================
    # MODEL PATHS
    # RELATIVE TO PROJECT ROOT
    # =========================
    MODEL_DIR: str = "WEIGHTS"
    GFPGAN_MODEL_PATH: str = "WEIGHTS/GFPGANv1.3.pth"
    REALESRGAN_MODEL_PATH: str = "WEIGHTS/RealESRGAN_x4plus.pth"
    
    # INSIGHTFACE MODEL
    INSIGHTFACE_MODEL_NAME: str = "buffalo_l"

    # =========================
    # PROCESSING LIMITS
    # MAX UPLOAD SIZE IN MB (CONVERTED TO BYTES BELOW)
    # =========================
    MAX_UPLOAD_SIZE_MB: int = 10
    DEFAULT_UPSCALE_FACTOR: int = 2

    # DERIVED VALUE: CONVERT MB TO BYTES
    @property
    def MAX_UPLOAD_SIZE_BYTES(self) -> int:
        return self.MAX_UPLOAD_SIZE_MB * 1024 * 1024

    # =========================
    # PYDANTIC SETTINGS CONFIG
    # LOADS VARIABLES FROM .env
    # extra="ignore" PREVENTS CRASHES FROM UNUSED VARIABLES
    # =========================
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
    
    # MAX CONCURRENT GPU TASKS
    # SET TO 1 FOR MOST CONSUMER GPUS (16GB VRAM OR LESS)
    # SET TO 2+ ONLY IF YOU HAVE A 3090/4090 OR A100
    MAX_CONCURRENT_REQUESTS: int = 1
    
    # MAX DIMENSION FOR INPUT IMAGES (PIXELS)
    MAX_INPUT_DIMENSION: int = 2048


# CREATE A SINGLE SETTINGS INSTANCE
settings = Settings()