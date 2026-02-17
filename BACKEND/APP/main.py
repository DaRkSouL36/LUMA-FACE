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

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"STARTING UP {settings.PROJECT_NAME}...")
    try:
        model_manager.load_all_models()
    except Exception as e:
        logger.critical(f"FAILED TO LOAD MODELS: {e}")
    
    logger.info("WARMING UP MODELS...")
    try:
        dummy_img = np.zeros((512, 512, 3), dtype=np.uint8)
        dummy_bytes = cv2.imencode('.jpg', dummy_img)[1].tobytes()
        from APP.SERVICES.pipeline import EnhancementPipeline
        EnhancementPipeline.process_image(dummy_bytes)
        logger.info("WARMUP COMPLETED. MODELS HOT.")
    except Exception as e:
        logger.warning(f"WARMUP FAILED (NON-CRITICAL): {e}")

    yield
    logger.info("SHUTTING DOWN...")
    model_manager.unload_all_models()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# --- UPDATED CORS ORIGINS ---
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://13.217.210.171:3000",
    "http://13.217.210.171",
]

if settings.BACKEND_CORS_ORIGINS:
    for origin in settings.BACKEND_CORS_ORIGINS:
        origins.append(str(origin))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["Status"])
async def health_check():
    return JSONResponse(status_code=200, content={"status": "healthy", "version": "1.0.0"})

@app.get("/", tags=["Status"])
async def root():
    return {"message": f"WELCOME TO {settings.PROJECT_NAME}", "docs": "/docs"}

app.include_router(api_router, prefix=settings.API_V1_STR)
