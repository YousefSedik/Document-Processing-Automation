from celery import shared_task
from document.models import Document

@shared_task
def process_document(document_id):
    document = Document.objects.get(id=document_id)
