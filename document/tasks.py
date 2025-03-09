from celery import shared_task
from .models import ServiceConfig
from .models import Document


@shared_task
def process_document_task(document_id):
    document = Document.objects.get(id=document_id)
    print(f"Processing document {document.id}")
    try:
        # Load selected services dynamically
        PDFToImages = ServiceConfig.objects.get(
            service_type="PDFToImagesService"
        ).get_service_instance()
        ExtractTextFromImage = ServiceConfig.objects.get(
            service_type="ImageToTextService"
        ).get_service_instance()
        IdentifyCategory = ServiceConfig.objects.get(
            service_type="IdentifyCategoryService"
        ).get_service_instance()
        FormatContent = ServiceConfig.objects.get(
            service_type="FormatContentService"
        ).get_service_instance()
        SummaryFromContent = ServiceConfig.objects.get(
            service_type="SummaryFromContentService"
        ).get_service_instance()
        ContentToJson = ServiceConfig.objects.get(
            service_type="ContentToJSONService"
        ).get_service_instance()
        if document.file_type == Document.FileType.PDF:
            files_paths = PDFToImages.pdf_to_images(document.file.path)
            print(f"Extracted {len(files_paths)} images from PDF")
        else:
            files_paths = [document.file.path]

        content = ""
        for image_path in files_paths:
            print(f"Extracting text from image: {image_path}")
            text = ExtractTextFromImage.image_to_text(image_path) or ""
            content += text + "\n"

        categories = IdentifyCategory.identify_category(content)
        print(f"Identified categories: {categories}")
        document.add_categories(categories)
        document.formatted_content = FormatContent.optimize_content(content)
        document.summary = SummaryFromContent.generate_summary(content)
        document.json_content = ContentToJson.content_to_json(
            document.formatted_content
        )
        document.status = Document.ProcessingStatus.PROCESSED
    except Exception as e:
        print(f"Failed to process document {document.id}: {e}")
        document.status = Document.ProcessingStatus.FAILED

    document.save()
