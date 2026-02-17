import torch
import gc
from APP.CORE.config import settings
from APP.CORE.logging import logger
from APP.MODELS.gfpgan import GFPGANWrapper
from APP.MODELS.realesrgan import RealESRGANWrapper
from APP.MODELS.insightface import InsightFaceWrapper


class ModelManager:
    """
    SINGLETON CLASS TO MANAGE ALL AI MODELS.
    ENSURES MODELS ARE LOADED ONLY ONCE AND SHARED ACROSS REQUESTS.
    """
    _instance = None

    def __new__(cls):
        # SINGLETON INITIALIZATION
        if cls._instance is None:
            cls._instance = super(ModelManager, cls).__new__(cls)
            cls._instance.gfpgan = None
            cls._instance.realesrgan = None
            cls._instance.insightface = None
        return cls._instance

    # ---------------------------------------------------------
    # MODEL LOADING
    # ---------------------------------------------------------
    def load_all_models(self):
        """
        LOADS ALL MODELS INTO MEMORY.
        CALLED ON APPLICATION STARTUP.
        """
        logger.info("INITIALIZING MODEL MANAGER...")

        # LOAD GFPGAN
        logger.info("LOADING GFPGAN...")
        self.gfpgan = GFPGANWrapper(
            model_path=settings.GFPGAN_MODEL_PATH,
            device=settings.DEVICE
        )
        self.gfpgan.load()

        # LOAD REAL-ESRGAN
        logger.info("LOADING REAL-ESRGAN...")
        self.realesrgan = RealESRGANWrapper(
            model_path=settings.REALESRGAN_MODEL_PATH,
            device=settings.DEVICE
        )
        self.realesrgan.load()

        # LOAD INSIGHTFACE
        logger.info("LOADING INSIGHTFACE...")
        self.insightface = InsightFaceWrapper(
            model_name=settings.INSIGHTFACE_MODEL_NAME,
            device=settings.DEVICE
        )
        self.insightface.load()

        logger.info("ALL MODELS LOADED AND READY.")

    # ---------------------------------------------------------
    # BACKWARD COMPATIBILITY METHODS
    # FIXES: 'ModelManager' object has no attribute 'enhance_face'
    # ---------------------------------------------------------
    def enhance_face(self, img):
        """
        FACE RESTORATION USING GFPGAN.
        USED BY OLD PIPELINE IMPLEMENTATIONS.
        """
        if self.gfpgan is None:
            raise RuntimeError("GFPGAN MODEL NOT LOADED")
        return self.gfpgan.predict(img)

    def upscale_image(self, img, scale=2):
        """
        IMAGE UPSCALING USING REAL-ESRGAN.
        OPTIONAL HELPER FOR PIPELINE.
        """
        if self.realesrgan is None:
            raise RuntimeError("REAL-ESRGAN MODEL NOT LOADED")
        return self.realesrgan.predict(img, outscale=scale)

    def get_face_embedding(self, img):
        """
        RETURNS FACE EMBEDDING USING INSIGHTFACE.
        """
        if self.insightface is None:
            raise RuntimeError("INSIGHTFACE MODEL NOT LOADED")
        return self.insightface.get_embedding(img)

    # ---------------------------------------------------------
    # MODEL UNLOAD / MEMORY CLEANUP
    # ---------------------------------------------------------
    def unload_all_models(self):
        """
        CLEARS MODELS FROM MEMORY AND FREES GPU.
        CALLED DURING SHUTDOWN.
        """
        logger.info("UNLOADING MODELS...")

        # REMOVE REFERENCES
        self.gfpgan = None
        self.realesrgan = None
        self.insightface = None

        # FORCE PYTHON GARBAGE COLLECTION
        gc.collect()

        # CLEAR CUDA CACHE IF AVAILABLE
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        logger.info("GPU MEMORY CLEARED.")


# GLOBAL SINGLETON INSTANCE
model_manager = ModelManager()
