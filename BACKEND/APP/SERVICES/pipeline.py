import numpy as np
import cv2
import logging
import time

from APP.CORE.config import settings
from APP.SERVICES.model_manager import model_manager
from APP.SERVICES.image_utils import ImageUtils
from APP.UTILS.metrics import MetricsCalculator

logger = logging.getLogger("face_enhancer")


class EnhancementPipeline:
    @staticmethod
    def process_image(image_bytes: bytes) -> dict:
        """
        MAIN FACE ENHANCEMENT PIPELINE.
        SYNCHRONOUS FUNCTION (CALLED INSIDE THREADPOOL).
        """
        start_time = time.time()
        logger.info("--- STARTING PIPELINE ---")

        try:
            # ---------------------------------------------------------
            # 1. DECODE IMAGE AND LIMIT SIZE
            # ---------------------------------------------------------
            original_img = ImageUtils.bytes_to_numpy(image_bytes)

            # LIMIT MAX SIZE TO PREVENT AWS OOM
            original_img = ImageUtils.constrain_image_size(
                original_img,
                settings.MAX_INPUT_DIMENSION
            )

            h, w = original_img.shape[:2]
            logger.info(f"IMAGE DECODED AND RESIZED. SHAPE: ({h}, {w}, 3)")

            # ---------------------------------------------------------
            # 2. GFPGAN FACE RESTORATION
            # ---------------------------------------------------------
            logger.info("STARTING GFPGAN RESTORATION...")
            restored_img = model_manager.enhance_face(original_img)
            logger.info("GFPGAN RESTORATION COMPLETED.")

            # ---------------------------------------------------------
            # 3. REAL-ESRGAN UPSCALING
            # ---------------------------------------------------------
            logger.info("STARTING REAL-ESRGAN UPSCALING...")
            upscaled_img = model_manager.upscale_image(restored_img)
            logger.info("REAL-ESRGAN UPSCALING COMPLETED.")

            # ---------------------------------------------------------
            # 4. METRICS
            # ---------------------------------------------------------
            logger.info("CALCULATING PERCEPTUAL METRICS...")
            metrics = MetricsCalculator.calculate_all(original_img, upscaled_img)

            metrics_response = {
                "psnr": float(metrics.get("psnr", 0.0)),
                "ssim": float(metrics.get("ssim", 0.0)),
                "lpips": float(metrics.get("lpips", 0.0)),
                "identity_score": float(metrics.get("identity_score", 0.0))
            }

            # ---------------------------------------------------------
            # 5. ENCODE FINAL IMAGE
            # ---------------------------------------------------------
            image_base64 = ImageUtils.numpy_to_base64(upscaled_img)

            # ---------------------------------------------------------
            # 6. TIMING
            # ---------------------------------------------------------
            total_time = time.time() - start_time
            logger.info(f"--- PIPELINE FINISHED IN {total_time:.2f}s ---")

            # ---------------------------------------------------------
            # 7. RETURN (FRONTEND FORMAT)
            # ---------------------------------------------------------
            return {
                "success": True,
                "message": "IMAGE ENHANCED SUCCESSFULLY",
                "image_base64": image_base64,
                "metrics": metrics_response,
                "processing_time_ms": int(total_time * 1000)
            }

        except Exception as e:
            total_time = time.time() - start_time
            logger.error(f"PIPELINE ERROR: {str(e)}")

            return {
                "success": False,
                "message": f"Processing failed: {str(e)}",
                "image_base64": "",
                "metrics": {
                    "psnr": 0.0,
                    "ssim": 0.0,
                    "lpips": 0.0,
                    "identity_score": 0.0
                },
                "processing_time_ms": int(total_time * 1000)
            }
