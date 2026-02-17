import time
import asyncio
from fastapi import APIRouter, UploadFile, File, HTTPException, status

from APP.SCHEMAS.enhancement import EnhancementResponse, EnhancementMetrics
from APP.SERVICES.pipeline import EnhancementPipeline
from APP.CORE.config import settings
from APP.CORE.logging import logger

router = APIRouter()

# GLOBAL SEMAPHORE
request_semaphore = asyncio.Semaphore(settings.MAX_CONCURRENT_REQUESTS)

@router.post(
    "/enhance",
    response_model=EnhancementResponse,
    status_code=status.HTTP_200_OK,
    summary="ENHANCE A FACE IMAGE"
)
async def enhance_image(file: UploadFile = File(...)):
    start_time = time.time()
    logger.info(f"RECEIVED REQUEST: {file.filename}")

    # Validate type
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(
            status_code=400,
            detail="ONLY JPEG AND PNG IMAGES ARE SUPPORTED."
        )

    file_bytes = await file.read()

    # Validate size
    if len(file_bytes) > settings.MAX_UPLOAD_SIZE_BYTES:
        raise HTTPException(
            status_code=413,
            detail="FILE TOO LARGE"
        )

    try:
        async with request_semaphore:
            logger.info("ACQUIRED GPU LOCK. PROCESSING...")
            from fastapi.concurrency import run_in_threadpool
            result = await run_in_threadpool(EnhancementPipeline.process_image, file_bytes)

        duration_ms = (time.time() - start_time) * 1000
        logger.info(f"REQUEST COMPLETED IN {duration_ms:.2f}ms")

        return EnhancementResponse(
            success=True,
            message="IMAGE ENHANCED SUCCESSFULLY",
            image_base64=result["image_base64"],
            metrics=EnhancementMetrics(**result["metrics"]),
            processing_time_ms=duration_ms
        )

    except Exception as e:
        logger.exception(f"INTERNAL SERVER ERROR: {e}")
        raise HTTPException(
            status_code=500,
            detail="IMAGE PROCESSING FAILED"
        )
