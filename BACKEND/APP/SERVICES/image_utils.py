import cv2
import base64
import numpy as np
from PIL import Image
import io

class ImageUtils:
    @staticmethod
    def bytes_to_numpy(image_bytes: bytes) -> np.ndarray:
        """
        CONVERTS RAW BYTES TO OPENCV IMAGE (BGR).
        """
        # CONVERT BYTES TO NUMPY ARRAY
        nparr = np.frombuffer(image_bytes, np.uint8)
        # DECODE IMAGE
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("FAILED TO DECODE IMAGE")
        return img

    @staticmethod
    def numpy_to_base64(img: np.ndarray) -> str:
        """
        CONVERTS OPENCV IMAGE (BGR) TO BASE64 STRING.
        """
        # ENCODE TO JPEG
        success, buffer = cv2.imencode('.jpg', img)
        if not success:
            raise ValueError("FAILED TO ENCODE IMAGE")
        # CONVERT TO BASE64
        img_str = base64.b64encode(buffer).decode('utf-8')
        return img_str

    @staticmethod
    def denoise_image(img: np.ndarray, strength: float = 3.0) -> np.ndarray:
        """
        APPLIES NON-LOCAL MEANS DENOISING.
        STRENGTH: HIGHER = MORE SMOOTHING (BUT LESS DETAIL).
        3.0 IS A SAFE DEFAULT FOR FACES.
        """
        return cv2.fastNlMeansDenoisingColored(
            img, 
            None, 
            h=strength, 
            hColor=strength, 
            templateWindowSize=7, 
            searchWindowSize=21
        )

    @staticmethod
    def resize_image(img: np.ndarray, target_shape: tuple) -> np.ndarray:
        """
        RESIZES IMAGE TO MATCH TARGET SHAPE (H, W).
        USED FOR METRICS CALCULATION.
        """
        h, w = target_shape[:2]
        return cv2.resize(img, (w, h), interpolation=cv2.INTER_CUBIC)

    @staticmethod
    def bgr_to_rgb(img: np.ndarray) -> np.ndarray:
        """
        CONVERTS BGR (OPENCV) TO RGB (MATPLOTLIB/TORCH).
        """
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)