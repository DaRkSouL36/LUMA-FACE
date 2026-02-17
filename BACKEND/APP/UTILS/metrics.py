import cv2
import torch
import lpips
import numpy as np
from skimage.metrics import structural_similarity as ssim_func
from skimage.metrics import peak_signal_noise_ratio as psnr_func
from APP.CORE.config import settings
from APP.SERVICES.image_utils import ImageUtils


class MetricsCalculator:
    # ---------------------------------------------------------
    # SINGLETON LPIPS MODEL (LOAD ONCE)
    # ---------------------------------------------------------
    _lpips_model = None

    @classmethod
    def get_lpips_model(cls):
        """
        RETURNS SHARED LPIPS MODEL INSTANCE.
        LOADS ONLY ON FIRST CALL.
        """
        if cls._lpips_model is None:
            device = torch.device(settings.DEVICE)
            cls._lpips_model = lpips.LPIPS(net='alex').to(device)
            cls._lpips_model.eval()
        return cls._lpips_model

    # ---------------------------------------------------------
    # PSNR
    # ---------------------------------------------------------
    @staticmethod
    def calculate_psnr(img1: np.ndarray, img2: np.ndarray) -> float:
        """
        CALCULATE PEAK SIGNAL-TO-NOISE RATIO.
        """
        if img1.shape != img2.shape:
            img2 = ImageUtils.resize_image(img2, img1.shape)

        return float(psnr_func(img1, img2, data_range=255))

    # ---------------------------------------------------------
    # SSIM
    # ---------------------------------------------------------
    @staticmethod
    def calculate_ssim(img1: np.ndarray, img2: np.ndarray) -> float:
        """
        CALCULATE STRUCTURAL SIMILARITY INDEX.
        """
        if img1.shape != img2.shape:
            img2 = ImageUtils.resize_image(img2, img1.shape)

        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        return float(ssim_func(gray1, gray2, data_range=255))

    # ---------------------------------------------------------
    # LPIPS
    # ---------------------------------------------------------
    @classmethod
    def calculate_lpips(cls, img1: np.ndarray, img2: np.ndarray) -> float:
        """
        CALCULATE PERCEPTUAL DISTANCE (LOWER IS BETTER).
        """
        device = torch.device(settings.DEVICE)
        loss_fn = cls.get_lpips_model()

        if img1.shape != img2.shape:
            img2 = ImageUtils.resize_image(img2, img1.shape)

        def preprocess(img):
            img = ImageUtils.bgr_to_rgb(img)
            img = (img / 127.5) - 1.0
            img = img.transpose((2, 0, 1))
            img = torch.from_numpy(img).float().unsqueeze(0)
            return img.to(device)

        tensor1 = preprocess(img1)
        tensor2 = preprocess(img2)

        with torch.no_grad():
            dist = loss_fn(tensor1, tensor2)

        return float(dist.item())

    # ---------------------------------------------------------
    # CALCULATE ALL METRICS (PIPELINE FIX)
    # ---------------------------------------------------------
    @classmethod
    def calculate_all(cls, img1: np.ndarray, img2: np.ndarray):
        """
        CALCULATES ALL METRICS SAFELY.
        PREVENTS PIPELINE CRASH IF ANY METRIC FAILS.
        """
        # PSNR
        try:
            psnr_val = cls.calculate_psnr(img1, img2)
        except Exception:
            psnr_val = 0.0

        # SSIM
        try:
            ssim_val = cls.calculate_ssim(img1, img2)
        except Exception:
            ssim_val = 0.0

        # LPIPS (CAN FAIL IF GPU MEMORY ISSUE)
        try:
            lpips_val = cls.calculate_lpips(img1, img2)
        except Exception:
            lpips_val = 0.0

        return {
            "psnr": round(float(psnr_val), 2),
            "ssim": round(float(ssim_val), 4),
            "lpips": round(float(lpips_val), 4),
            # IDENTITY WILL BE FILLED BY PIPELINE IF USED
            "identity_score": 0.0
        }
