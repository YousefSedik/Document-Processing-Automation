from celery import shared_task
from document.utils.PDFToImagesService.PDFToImageUsingPackage import (
    PDFToImageUsingPDF2ImagePackage,
)
from document.utils.ImageToTextService.TesseractImageToTextService import (
    TesseractImageToTextService,
)
from document.utils.IdentifyCategoryService.IdentifyCategoryUsingGeminiAPI import (
    IdentifyCategoryUsingGeminiAPI,
)
from document.utils.FormatContentService.FormatContentServiceUsingGeminiAPI import (
    FormatContentServiceUsingGeminiAPI,
)
from document.models import Document


@shared_task
def process_document_task(document_id):
    document = Document.objects.get(id=document_id)
    print(f"Processing document {document.id}")
    # Defining Services
    PDFToImages = PDFToImageUsingPDF2ImagePackage()
    ExtractTextFromImage = TesseractImageToTextService()
    IdentifyCategory = IdentifyCategoryUsingGeminiAPI()
    FormatContent = FormatContentServiceUsingGeminiAPI()
    try:
        if document.file_type == Document.FileType.PDF:
            files_paths = PDFToImages.pdf_to_images(document.file.path)
            print(f"Extracted {len(files_paths)} images from PDF")
        else:
            files_paths = [document.file.path]
        summary = ""
        for image_path in files_paths:
            print(f"Extracting text from image: {image_path}")
            text = ExtractTextFromImage.image_to_text(image_path)
            if text is None:
                text = ""
            summary = summary + text + "\n"
        categories = IdentifyCategory.identify_category(summary)
        print(f"Identified categories: {categories}")
        document.add_categories(categories)
        document.summary = FormatContent.optimize_content(summary)
        document.status = Document.ProcessingStatus.PROCESSED
    except Exception as e:
        print(f"Failed to process document {document.id}: {e}")
        document.status = Document.ProcessingStatus.FAILED
    document.save()
