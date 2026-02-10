import os
import torch
import numpy as np
from gfpgan import GFPGANer
from APP.CORE.logging import logger
from APP.MODELS.base import BaseModel

class GFPGANWrapper(BaseModel):
    def load(self):
        """
        INITIALIZES THE GFPGANER INSTANCE.
        """
        if not os.path.exists(self.model_path):
            logger.error(f"GFPGAN WEIGHTS NOT FOUND AT: {self.model_path}")
            raise FileNotFoundError(f"MISSING WEIGHTS: {self.model_path}")

        try:
            logger.info(f"LOADING GFPGAN FROM {self.model_path} ON {self.device}...")
            
            # INITIALIZE THE GFPGANER
            # UPSCALE=1 PREVENTS INTERNAL UPSCALING (WE DO IT SEPARATELY)
            # ARCH='clean' IS STANDARD FOR V1.3
            # CHANNEL_MULTIPLIER=2 IS REQUIRED FOR V1.3
            self.model = GFPGANer(
                model_path=self.model_path,
                upscale=1,
                arch='clean',
                channel_multiplier=2,
                bg_upsampler=None, # WE DISABLE INTERNAL BG UPSAMPLER
                device=self.device
            )
            logger.info("GFPGAN LOADED SUCCESSFULLY.")
            
        except Exception as e:
            logger.error(f"FAILED TO LOAD GFPGAN: {e}")
            raise e

    def predict(self, img: np.ndarray) -> np.ndarray:
        """
        RESTORES FACES IN THE INPUT IMAGE.
        INPUT: NUMPY ARRAY (BGR)
        OUTPUT: NUMPY ARRAY (BGR)
        """
        if self.model is None:
            raise RuntimeError("GFPGAN MODEL NOT LOADED")

        # GFPGANER.ENHANCE RETURNS: (CROPPED_FACES, RESTORED_FACES, RESTORED_IMG)
        # WE ONLY CARE ABOUT THE FINAL RESTORED IMAGE
        _, _, restored_img = self.model.enhance(
            img, 
            has_aligned=False, 
            only_center_face=False, 
            paste_back=True,
            weight=0.5 # BALANCE BETWEEN ORIGINAL AND RESTORED (0.5 IS SAFE)
        )
        
        return restored_img