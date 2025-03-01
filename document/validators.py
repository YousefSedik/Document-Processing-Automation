from rest_framework.exceptions import ValidationError


def validate_file_extension(value):
    if not value.name.lower().endswith((".pdf", ".png", ".jpg", ".jpeg")):
        raise ValidationError("File type not supported")


def validate_file_size(value):
    if value.size > 100 * 1024 * 1024:
        raise ValidationError("File size should not exceed 100MB")
