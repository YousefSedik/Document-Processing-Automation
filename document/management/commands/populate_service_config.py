from django.core.management.base import BaseCommand
from document.models import ServiceConfig


class Command(BaseCommand):
    def handle(self, *args, **options):
        ServiceConfig.objects.create(
            service_type="PDFToImagesService",
            implementation="document.utils.PDFToImagesService.PDFToImageUsingPDF2ImagePackage",
        )

        ServiceConfig.objects.create(
            service_type="ImageToTextService",
            implementation="document.utils.ImageToTextService.TesseractImageToTextService",
        )

        ServiceConfig.objects.create(
            service_type="IdentifyCategoryService",
            implementation="document.utils.IdentifyCategoryService.IdentifyCategoryUsingGeminiAPI",
        )

        ServiceConfig.objects.create(
            service_type="FormatContentService",
            implementation="document.utils.FormatContentService.FormatContentServiceUsingGeminiAPI",
        )

        ServiceConfig.objects.create(
            service_type="SummaryFromContentService",
            implementation="document.utils.SummaryFromContentService.SummaryFromContentGeminiAPI",
        )

        ServiceConfig.objects.create(
            service_type="ContentToJSONService",
            implementation="document.utils.ContentToJSONService.ContentToJSONGeminiAPI",
        )
