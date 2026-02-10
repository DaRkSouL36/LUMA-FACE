from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logging import logger

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
    
    model_manager.load_models()
    
    logger.info("SYSTEM READY.")
    
    yield
    
    # --- SHUTDOWN LOGIC ---
    logger.info("SHUTTING DOWN...")
    model_manager.unload_models()

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
# MIDDLEWARE
# -----------------------------------------------------------------------------
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
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
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "docs": "/docs"
    }

app.include_router(api_router, prefix=settings.API_V1_STR)