import cv2  
import numpy as np
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from APP.CORE.config import settings
from APP.CORE.logging import logger
from APP.API.V1.api import api_router
from APP.SERVICES.model_manager import model_manager

# -----------------------------------------------------------------------------
# LIFESPAN CONTEXT MANAGER
# -----------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    LIFECYCLE EVENTS FOR THE APPLICATION.
    1. STARTUP: LOAD MODELS, CONNECT TO DB (IF ANY), WARMUP CACHES.
    2. YIELD: APPLICATION RUNS.
    3. SHUTDOWN: CLEANUP RESOURCES.
    """
    # --- STARTUP LOGIC ---
    logger.info(f"STARTING UP {settings.PROJECT_NAME}...")
    logger.info(f"RUNNING ON DEVICE: {settings.DEVICE}")
    
    try:
        # LOADING MODELS
        model_manager.load_all_models()
        pass
    except Exception as e:
        logger.critical(f"FAILED TO LOAD MODELS: {e}")
        # WE DO NOT RAISE HERE TO ALLOW SERVER TO START SO WE CAN SEE LOGS
    
    # --- WARMUP ROUTINE (OPTIMIZATION) ---
    # RUNS A DUMMY IMAGE THROUGH THE PIPELINE TO INITIALIZE CUDA KERNELS
    logger.info("WARMING UP MODELS...")
    try:
        # 1. CREATE A TINY DUMMY IMAGE (512x512 BLACK SQUARE)
        dummy_img = np.zeros((512, 512, 3), dtype=np.uint8)
        dummy_bytes = cv2.imencode('.jpg', dummy_img)[1].tobytes()
        
        # 2. RUN PIPELINE (SILENTLY IGNORE RESULT)
        # IMPORT INSIDE FUNCTION TO AVOID CIRCULAR IMPORT ISSUES
        from APP.SERVICES.pipeline import EnhancementPipeline
        
        # EXECUTE PIPELINE (THIS WILL TRIGGER MODEL COMPILATION/ALLOCATION)
        # NOTE: THIS WILL RUN FAST IN MOCK_MODE, OR TAKE ~5S IN REAL MODE
        EnhancementPipeline.process_image(dummy_bytes)
        
        logger.info("WARMUP COMPLETED. MODELS HOT.")
    except Exception as e:
        logger.warning(f"WARMUP FAILED (NON-CRITICAL): {e}")

    logger.info("SYSTEM READY.")
    
    yield
    
    # --- SHUTDOWN LOGIC ---
    logger.info("SHUTTING DOWN...")
    # UNLOAD MODELS TO FREE MEMORY
    model_manager.unload_all_models()
    
# -----------------------------------------------------------------------------
# APP INITIALIZATION
# -----------------------------------------------------------------------------
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
    docs_url="/docs", # SWAGGER UI
    redoc_url="/redoc"
)

# -----------------------------------------------------------------------------
# MIDDLEWARE (CORS CONFIGURATION)
# -----------------------------------------------------------------------------
# EXPLICITLY ALLOW LOCALHOST:3000 TO FIX BROWSER CORS ERRORS
origins = [
    "http://localhost:3000",      # REACT FRONTEND
    "http://127.0.0.1:3000",      # REACT FRONTEND (ALTERNATIVE IP)
]

# IF SETTINGS HAS EXTRA ORIGINS, ADD THEM TOO
if settings.BACKEND_CORS_ORIGINS:
    for origin in settings.BACKEND_CORS_ORIGINS:
        origins.append(str(origin))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],          # ALLOW ALL METHODS (POST, GET, ETC.)
    allow_headers=["*"],          # ALLOW ALL HEADERS
)

# -----------------------------------------------------------------------------
# BASE ROUTES
# -----------------------------------------------------------------------------
@app.get("/health", tags=["Status"])
async def health_check():
    """
    LIGHTWEIGHT HEALTH CHECK FOR ORCHESTRATORS.
    """
    return JSONResponse(
        status_code=200, 
        content={"status": "healthy", "version": "1.0.0"}
    )

@app.get("/", tags=["Status"])
async def root():
    """
    ROOT ENDPOINT.
    """
    return {
        "message": f"WELCOME TO {settings.PROJECT_NAME}",
        "docs": "/docs"
    }

# INCLUDE ROUTER
app.include_router(api_router, prefix=settings.API_V1_STR)