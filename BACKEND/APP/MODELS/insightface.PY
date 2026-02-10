import numpy as np
import insightface
from insightface.app import FaceAnalysis
from APP.CORE.logging import logger
from APP.MODELS.base import BaseModel

class InsightFaceWrapper(BaseModel):
    def __init__(self, model_name: str, device: str):
        # INSIGHTFACE DOESN'T USE A SINGLE FILE PATH LIKE .PTH
        # IT USES A MODEL DIRECTORY (~/.insightface/models)
        super().__init__(model_path=model_name, device=device)

    def load(self):
        """
        LOADS THE FACE ANALYSIS APP (DETECTION + RECOGNITION).
        """
        try:
            logger.info(f"LOADING INSIGHTFACE ({self.model_path}) ON {self.device}...")
            
            # PROVIDERS: CUDA OR CPU
            providers = ['CUDAExecutionProvider'] if self.device.type == 'cuda' else ['CPUExecutionProvider']

            self.model = FaceAnalysis(
                name=self.model_path, 
                providers=providers,
                allowed_modules=['detection', 'recognition'] # WE ONLY NEED THESE
            )
            
            # PREPARE MODELS (CTX_ID=0 FOR GPU 0, -1 FOR CPU)
            ctx_id = 0 if self.device.type == 'cuda' else -1
            self.model.prepare(ctx_id=ctx_id, det_size=(640, 640))
            
            logger.info("INSIGHTFACE LOADED SUCCESSFULLY.")

        except Exception as e:
            logger.error(f"FAILED TO LOAD INSIGHTFACE: {e}")
            raise e

    def get_embedding(self, img: np.ndarray):
        """
        RETURNS THE EMBEDDING OF THE LARGEST FACE IN THE IMAGE.
        """
        if self.model is None:
            raise RuntimeError("INSIGHTFACE NOT LOADED")
            
        faces = self.model.get(img)
        if not faces:
            return None
            
        # SORT BY AREA TO GET THE MAIN FACE (LARGEST)
        faces.sort(key=lambda x: (x.bbox[2]-x.bbox[0]) * (x.bbox[3]-x.bbox[1]), reverse=True)
        return faces[0].embedding