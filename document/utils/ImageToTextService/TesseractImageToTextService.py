from .ImageToTextService import ImageToTextServiceBase
from PIL import Image
import pytesseract

class TesseractImageToTextService(ImageToTextServiceBase):
    @staticmethod
    def image_to_text(image_path: str) -> str:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
