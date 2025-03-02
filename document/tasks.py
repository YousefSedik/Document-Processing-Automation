from celery import shared_task
from django.apps import apps
from document.utils.PDFToImagesService.PDFToImageUsingPackage import (
    PDFToImageUsingPDF2ImagePackage,
)
from document.models import Document


@shared_task
def process_document_task(document_id):
    document = Document.objects.get(id=document_id)
    print(f"Processing document {document.id}")
    try:
        files_paths = PDFToImageUsingPDF2ImagePackage.pdf_to_images(document.file.path)
        print(f"Extracted {len(files_paths)} images from PDF")
        document.status = Document.ProcessingStatus.PROCESSED
    except Exception as e:
        print(f"Failed to process document {document.id}: {e}")
        document.status = Document.ProcessingStatus.FAILED
    document.save()
