from abc import ABC, abstractmethod
import torch
import numpy as np

class BaseModel(ABC):
    """
    ABSTRACT BASE CLASS FOR ALL AI MODELS.
    ENSURES CONSISTENT INTERFACE FOR LOADING AND INFERENCE.
    """
    
    def __init__(self, model_path: str, device: str):
        self.model_path = model_path
        self.device = torch.device(device)
        self.model = None

    @abstractmethod
    def load(self):
        """
        LOAD WEIGHTS INTO MEMORY.
        MUST BE CALLED AT STARTUP.
        """
        pass

    @abstractmethod
    def predict(self, input_data):
        """
        RUN INFERENCE.
        """
        pass