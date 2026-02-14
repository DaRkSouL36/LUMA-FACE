import time
import asyncio
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.concurrency import run_in_threadpool

from APP.SCHEMAS.enhancement import EnhancementResponse, EnhancementMetrics
from APP.SERVICES.pipeline import EnhancementPipeline
from APP.CORE.config import settings
from APP.CORE.logging import logger

router = APIRouter()

# GLOBAL SEMAPHORE
# WE INITIALIZE IT OUTSIDE THE ENDPOINT SO IT'S SHARED ACROSS REQUESTS
# THIS LIMITS CONCURRENT GPU USAGE TO PREVENT OOM ERRORS
request_semaphore = asyncio.Semaphore(settings.MAX_CONCURRENT_REQUESTS)

@router.post(
    "/enhance",
    response_model=EnhancementResponse,
    status_code=status.HTTP_200_OK,
    summary="ENHANCE A FACE IMAGE",
    description="UPLOADS AN IMAGE, PROCESSES IT THROUGH GFPGAN AND REAL-ESRGAN, AND RETURNS THE RESULT WITH METRICS."
)
async def enhance_image(
    file: UploadFile = File(...)
):
    """
    MAIN ENHANCEMENT ENDPOINT.
    HANDLES FILE UPLOAD, VALIDATION, AND PIPELINE EXECUTION.
    INCLUDES CONCURRENCY CONTROL VIA SEMAPHORE.
    """
    start_time = time.time()
    logger.info(f"RECEIVED REQUEST: {file.filename}")

    # 1. VALIDATION
    # CHECK FILE TYPE
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        logger.warning(f"INVALID FILE TYPE: {file.content_type}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ONLY JPEG AND PNG IMAGES ARE SUPPORTED."
        )

    # CHECK FILE SIZE (READING INTO MEMORY FIRST)
    # NOTE: FOR VERY LARGE FILES, STREAMING IS BETTER, BUT FOR <10MB IMAGES, READ() IS FINE.
    file_bytes = await file.read()
    if len(file_bytes) > settings.MAX_UPLOAD_SIZE_BYTES:
        logger.warning(f"FILE TOO LARGE: {len(file_bytes)} BYTES")
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"FILE SIZE EXCEEDS LIMIT OF {settings.MAX_UPLOAD_SIZE_BYTES / 1024 / 1024}MB"
        )

    try:
        # 2. PROCESS IMAGE (NON-BLOCKING WITH CONCURRENCY CONTROL)
        # WE USE A SEMAPHORE TO LIMIT CONCURRENT GPU TASKS.
        # IF THE SEMAPHORE IS FULL, THIS LINE WILL WAIT HERE UNTIL A SLOT OPENS.
        
        async with request_semaphore:
            logger.info(f"ACQUIRED GPU LOCK. PROCESSING IN THREADPOOL...")
            
            # WE USE RUN_IN_THREADPOOL TO PREVENT BLOCKING THE ASYNC EVENT LOOP
            # THIS RUNS THE SYNCHRONOUS 'PROCESS_IMAGE' FUNCTION IN A WORKER THREAD
            result = await run_in_threadpool(
                EnhancementPipeline.process_image, 
                image_bytes=file_bytes
            )

        # 3. CALCULATE TIMING
        end_time = time.time()
        duration_ms = (end_time - start_time) * 1000
        logger.info(f"REQUEST COMPLETED IN {duration_ms:.2f}ms")

        # 4. CONSTRUCT RESPONSE
        return EnhancementResponse(
            success=True,
            message="IMAGE ENHANCED SUCCESSFULLY.",
            image_base64=result["image_base64"],
            metrics=EnhancementMetrics(**result["metrics"]),
            processing_time_ms=duration_ms
        )

    except ValueError as ve:
        # HANDLE KNOWN ERRORS (E.G. DECODING FAILED)
        logger.error(f"VALIDATION ERROR: {ve}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        # HANDLE UNEXPECTED SERVER ERRORS
        logger.exception(f"INTERNAL SERVER ERROR: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AN ERROR OCCURRED DURING IMAGE PROCESSING."
        )