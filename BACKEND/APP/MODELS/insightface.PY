import numpy as np
from insightface.app import FaceAnalysis
from APP.CORE.logging import logger
from APP.MODELS.base import BaseModel


class InsightFaceWrapper(BaseModel):
    def __init__(self, model_name: str, device):
        # INSIGHTFACE USES A MODEL NAME (E.G., antelopev2)
        # MODELS ARE DOWNLOADED AUTOMATICALLY TO ~/.insightface/models
        super().__init__(model_path=model_name, device=device)

    def load(self):
        """
        LOAD INSIGHTFACE USING OFFICIAL INITIALIZATION FLOW
        """
        try:
            logger.info(f"LOADING INSIGHTFACE ({self.model_path}) ON {self.device}...")

            # SELECT PROVIDERS
            if str(self.device) == "cuda":
                providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
                ctx_id = 0
            else:
                providers = ['CPUExecutionProvider']
                ctx_id = -1

            # INITIALIZE APP
            self.model = FaceAnalysis(
                name=self.model_path, 
                providers=providers,
                allowed_modules=['detection', 'recognition'] 
            )

            # PREPARE (THIS TRIGGERS MODEL LOAD)
            self.model.prepare(ctx_id=ctx_id, det_size=(640, 640))

            logger.info("INSIGHTFACE LOADED SUCCESSFULLY.")

        except Exception as e:
            logger.exception(f"FAILED TO LOAD INSIGHTFACE: {e}")
            raise e

    def predict(self, img: np.ndarray):
        """
        REQUIRED BY BASEMODEL.
        RETURNS ALL DETECTED FACES.
        """
        if self.model is None:
            raise RuntimeError("INSIGHTFACE NOT LOADED")

        faces = self.model.get(img)
        return faces

    def get_embedding(self, img: np.ndarray):
        """
        RETURNS THE EMBEDDING OF THE LARGEST FACE IN THE IMAGE.
        """
        faces = self.predict(img)
        if not faces:
            return None

        # SORT BY FACE AREA (LARGEST FIRST)
        faces.sort(
            key=lambda x: (x.bbox[2] - x.bbox[0]) * (x.bbox[3] - x.bbox[1]),
            reverse=True
        )

        return faces[0].embedding