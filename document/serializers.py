from rest_framework import serializers
from .models import Document


class DocumentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["file"]


class DocumentRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            "id",
            "created_at",
            "status",
            "summary",
            "content",
            "categories",
            "size",
        ]


class DocumentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id", "file", "file_type", "status", "created_at", "size"]
