from .validators import validate_file_extension, validate_file_size
from django.contrib.auth import get_user_model
from django.db import models
import os
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    content = models.JSONField(blank=True, null=True)
    file_type = models.CharField(max_length=10, choices=FileType.choices)
    file = models.FileField(
        upload_to="documents/", validators=[validate_file_extension, validate_file_size]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def size(self):
        return self.file.size

    @property
    def file_name(self):
        return os.path.basename(self.file.name)

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

from .tasks import process_document_task

@receiver(post_save, sender=Document)
def trigger_document_processing(sender, instance, created, **kwargs):
    if created:  # Only trigger task for new documents
        process_document_task.delay(instance.id)
