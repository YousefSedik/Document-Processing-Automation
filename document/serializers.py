from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id", "file_name", "file_type", "created_at", "status", "size"]


class DocumentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["file"]

class DocumentRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
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
