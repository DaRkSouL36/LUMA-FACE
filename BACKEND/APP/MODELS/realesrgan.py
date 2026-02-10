import os
import torch
import numpy as np
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer
from APP.CORE.logging import logger
from APP.MODELS.base import BaseModel

class RealESRGANWrapper(BaseModel):
    def load(self):
        """
        INITIALIZES REAL-ESRGAN WITH X4PLUS ARCHITECTURE.
        """
        if not os.path.exists(self.model_path):
            logger.error(f"REAL-ESRGAN WEIGHTS NOT FOUND AT: {self.model_path}")
            raise FileNotFoundError(f"MISSING WIEGHTS: {self.model_path}")

        try:
            logger.info(f"LOADING REAL-ESRGAN FROM {self.model_path} ON {self.device}...")

            # DEFINE THE NETWORK ARCHITECTURE (RRDBNET) FOR X4PLUS
            model_arch = RRDBNet(
                num_in_ch=3, 
                num_out_ch=3, 
                num_feat=64, 
                num_block=23, 
                num_grow_ch=32, 
                scale=4
            )

            # USE FP16 IF ON GPU
            use_half = True if self.device.type == 'cuda' else False

            self.model = RealESRGANer(
                scale=4,
                model_path=self.model_path,
                model=model_arch,
                tile=0, # 0 = NO TILING (FASTER, BUT HIGHER VRAM). USE 400 IF OOM.
                tile_pad=10,
                pre_pad=0,
                half=use_half,
                device=self.device
            )
            logger.info("REAL-ESRGAN LOADED SUCCESSFULLY.")

        except Exception as e:
            logger.error(f"FAILED TO LOAD REAL-ESRGAN: {e}")
            raise e

    def predict(self, img: np.ndarray, outscale: float = 2.0) -> np.ndarray:
        """
        UPSCALES THE IMAGE.
        INPUT: NUMPY ARRAY (BGR)
        OUTPUT: NUMPY ARRAY (BGR)
        """
        if self.model is None:
            raise RuntimeError("REAL-ESRGAN MODEL NOT LOADED")

        # ENHANCE RETURNS (OUTPUT, IMAGE_MODE)
        output, _ = self.model.enhance(img, outscale=outscale)
        return output