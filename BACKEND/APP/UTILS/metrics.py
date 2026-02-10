import cv2
import torch
import lpips
import numpy as np
from skimage.metrics import structural_similarity as ssim_func
from skimage.metrics import peak_signal_noise_ratio as psnr_func
from APP.CORE.config import settings
from APP.SERVICES.image_utils import ImageUtils

class MetricsCalculator:
    _lpips_model = None

    @classmethod
    def get_lpips_model(cls):
        """
        SINGLETON ACCESS TO LPIPS MODEL TO AVOID RELOADING.
        """
        if cls._lpips_model is None:
            # USING ALEXNET FOR SPEED
            device = torch.device(settings.DEVICE)
            cls._lpips_model = lpips.LPIPS(net='alex').to(device)
        return cls._lpips_model

    @staticmethod
    def calculate_psnr(img1: np.ndarray, img2: np.ndarray) -> float:
        """
        CALCULATE PEAK SIGNAL-TO-NOISE RATIO.
        IMG1, IMG2: NUMPY ARRAYS (BGR)
        """
        # IMAGES MUST BE SAME SIZE
        if img1.shape != img2.shape:
            img2 = ImageUtils.resize_image(img2, img1.shape)
        
        return float(psnr_func(img1, img2, data_range=255))

    @staticmethod
    def calculate_ssim(img1: np.ndarray, img2: np.ndarray) -> float:
        """
        CALCULATE STRUCTURAL SIMILARITY INDEX.
        """
        if img1.shape != img2.shape:
            img2 = ImageUtils.resize_image(img2, img1.shape)
            
        # CONVERT TO GRAYSCALE FOR SSIM
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        
        return float(ssim_func(gray1, gray2, data_range=255))

    @classmethod
    def calculate_lpips(cls, img1: np.ndarray, img2: np.ndarray) -> float:
        """
        CALCULATE PERCEPTUAL SIMILARITY (LOWER IS BETTER).
        REQUIRES CONVERSION TO TENSOR [-1, 1].
        """
        device = torch.device(settings.DEVICE)
        loss_fn = cls.get_lpips_model()

        if img1.shape != img2.shape:
            img2 = ImageUtils.resize_image(img2, img1.shape)

        # PREPROCESS: BGR -> RGB -> NORMALIZE [-1, 1] -> TENSOR -> GPU
        def preprocess(img):
            img = ImageUtils.bgr_to_rgb(img)
            img = (img / 127.5) - 1.0
            img = img.transpose((2, 0, 1)) # HWC -> CHW
            img = torch.from_numpy(img).float().unsqueeze(0)
            return img.to(device)

        tensor1 = preprocess(img1)
        tensor2 = preprocess(img2)

        with torch.no_grad():
            dist = loss_fn(tensor1, tensor2)
        
        return float(dist.item())