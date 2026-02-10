from APP.CORE.config import settings
from APP.CORE.logging import logger
from APP.MODELS.gfpgan import GFPGANWrapper
from APP.MODELS.realesrgan import RealESRGANWrapper
from APP.MODELS.insightface import InsightFaceWrapper

class ModelManager:
    """
    SINGLETON CLASS TO MANAGE AI MODELS.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelManager, cls).__new__(cls)
            cls._instance.gfpgan = None
            cls._instance.realesrgan = None
            cls._instance.insightface = None
        return cls._instance

    def load_all_models(self):
        """
        LOADS ALL MODELS INTO MEMORY.
        CALLED ONCE AT STARTUP.
        """
        logger.info("INITIALIZING MODEL MANAGER...")

        # 1. LOAD GFPGAN
        self.gfpgan = GFPGANWrapper(
            model_path=settings.GFPGAN_MODEL_PATH,
            device=settings.DEVICE
        )
        self.gfpgan.load()

        # 2. LOAD REAL-ESRGAN
        self.realesrgan = RealESRGANWrapper(
            model_path=settings.REALESRGAN_MODEL_PATH,
            device=settings.DEVICE
        )
        self.realesrgan.load()

        # 3. LOAD INSIGHTFACE
        self.insightface = InsightFaceWrapper(
            model_name=settings.INSIGHTFACE_MODEL_NAME,
            device=settings.DEVICE
        )
        self.insightface.load()
        
        logger.info("ALL MODELS LOADED AND READY.")

# GLOBAL INSTANCE
model_manager = ModelManager()