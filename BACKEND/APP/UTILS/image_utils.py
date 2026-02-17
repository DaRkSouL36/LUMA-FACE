import cv2
import numpy as np
import base64

class ImageUtils:

    @staticmethod
    def bytes_to_numpy(image_bytes: bytes) -> np.ndarray:
        np_arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Invalid image bytes")
        return img

    @staticmethod
    def constrain_image_size(img: np.ndarray, max_dim: int) -> np.ndarray:
        h, w = img.shape[:2]
        if max(h, w) <= max_dim:
            return img
        
        scale = max_dim / max(h, w)
        new_size = (int(w * scale), int(h * scale))
        return cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)

    @staticmethod
    def numpy_to_base64(img: np.ndarray) -> str:
        _, buffer = cv2.imencode('.jpg', img)
        return base64.b64encode(buffer).decode("utf-8")
