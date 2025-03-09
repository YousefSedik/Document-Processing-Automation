from .validators import (
    validate_file_extension,
    validate_file_size,
)
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
import importlib

import os


User = get_user_model()


class Document(models.Model):
    class ProcessingStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PROCESSED = "PROCESSED", "Processed"
        FAILED = "FAILED", "Failed"

    class FileType(models.TextChoices):
        PDF = "PDF", "PDF"
        IMAGE = "IMAGE", "Image"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=ProcessingStatus.choices,
        default=ProcessingStatus.PENDING,
    )
    summary = models.TextField(blank=True, null=True)
    formatted_content = models.TextField(blank=True, null=True)
    json_content = models.JSONField(blank=True, null=True)
    file_type = models.CharField(max_length=10, choices=FileType.choices)
    file = models.FileField(
        upload_to="documents/", validators=[validate_file_extension, validate_file_size]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def size(self):
        try:
            size_in_bytes = self.file.size
            size_in_kb = size_in_bytes / 1024
            size_in_mb = size_in_kb / 1024
            return f"{size_in_mb:.2f} mb"
        except FileNotFoundError:
            return ""

    @property
    def file_name(self):
        return os.path.basename(self.file.name)

    def add_categories(self, categories: list[str]):
        for category in categories:
            try:
                self.categories.add(Category.objects.get(name=category))
            except Category.DoesNotExist:
                print(f"Category {category} does not exist")

    def save(self, *args, **kwargs):
        if not self.file_type:
            self.file_type = (
                Document.FileType.PDF
                if self.file.name.lower().endswith(".pdf")
                else Document.FileType.IMAGE
            )
        super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=["user"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.file.name} - {self.status}"


class Category(models.Model):
    name = models.CharField(max_length=255)
    documents = models.ManyToManyField(Document, related_name="categories")

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name


class ServiceConfig(models.Model):
    class ServiceType(models.TextChoices):
        PDF_TO_IMAGES = "PDFToImagesService", "PDF To Images"
        IMAGE_TO_TEXT = "ImageToTextService", "Extract Text From Image"
        IDENTIFY_CATEGORY = "IdentifyCategoryService", "Identify Category"
        FORMAT_CONTENT = "FormatContentService", "Format Content"
        SUMMARY_FROM_CONTENT = "SummaryFromContentService", "Summarize Content"
        CONTENT_TO_JSON = "ContentToJSONService", "Convert Content to JSON"

    service_type = models.CharField(max_length=50, choices=ServiceType, unique=True)
    implementation = models.CharField(
        max_length=255,
        help_text="Enter the full module path, e.g., 'document.utils.PDFToImagesService.PDFToImageUsingPDF2ImagePackage'",
    )

    def clean(self):
        """Validate that the implementation can be imported."""
        try:
            module_name, class_name = self.implementation.rsplit(".", 1)
            module = importlib.import_module(module_name)
            if not hasattr(module, class_name):
                raise ValidationError(
                    f"Class '{class_name}' not found in '{module_name}'"
                )
        except Exception as e:
            raise ValidationError(f"Unable to import {self.implementation}: {e}")

    def save(self, *args, **kwargs):
        self.clean()  # Call clean before saving to enforce validation
        super().save(*args, **kwargs)

    def get_service_instance(self):
        """Dynamically imports and initializes the selected service class"""
        module_name, class_name = self.implementation.rsplit(".", 1)
        module = importlib.import_module(module_name)
        service_class = getattr(module, class_name)
        return service_class()

    def __str__(self):
        return f"{self.get_service_type_display()} -> {self.implementation}"


from .tasks import process_document_task


@receiver(post_save, sender=Document)
def trigger_document_processing(sender, instance, created, **kwargs):
    if created:  # Only trigger task for new documents
        process_document_task.delay(instance.id)
