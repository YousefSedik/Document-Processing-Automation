from abc import ABC, abstractmethod
from PIL import Image
import pytesseract


class ImageToTextServiceBase(ABC):
    @abstractmethod
    def image_to_text(image_path: str) -> str:
        pass