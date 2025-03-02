from .PDFToImagesServiceBase import PDFToImagesServiceBase
from pdf2image import convert_from_path
from pathlib import Path
import os


class PDFToImageUsingPDF2ImagePackage(PDFToImagesServiceBase):

    @staticmethod
    def pdf_to_images(pdf_path: str) -> list[str]:
        """Converts a PDF to images and saves them in a new folder.
        Args:
            pdf_path (str): Path to the PDF file.

        Returns:
            list[str]: List of saved image file paths.

        """
        pdf_path: Path = Path(pdf_path)

        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        print("Processing PDF:", pdf_path)

        images = convert_from_path(str(pdf_path))  # Convert PDF to images
        folder_path = pdf_path.with_suffix("")  # Remove `.pdf` extension from path

        folder_path.mkdir(parents=True, exist_ok=True)  # Create output directory

        image_paths = []
        for i, image in enumerate(images):
            image_path = folder_path / f"page_{i}.jpg"
            image.save(image_path, "JPEG")
            image_paths.append(str(image_path))
            print(f"Saved image: {image_path}")

        return image_paths
