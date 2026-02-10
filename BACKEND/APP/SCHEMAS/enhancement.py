from pydantic import BaseModel
from typing import Dict, Optional

class EnhancementMetrics(BaseModel):
    psnr: float
    ssim: float
    lpips: float
    identity_score: float

class EnhancementResponse(BaseModel):
    success: bool
    message: str
    image_base64: Optional[str] = None
    metrics: Optional[EnhancementMetrics] = None
    processing_time_ms: float