from abc import ABC, abstractmethod


class PDFToImagesServiceBase(ABC):
    @abstractmethod
    def pdf_to_images(self, pdf_path: str) -> list[str]:
        raise NotImplementedError
