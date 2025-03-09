from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ["id", "file_name", "file_type", "created_at", "status", "size"]

    def get_status(self, obj):
        return obj.get_status_display()


class DocumentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["file"]


class DocumentRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    categories = serializers.StringRelatedField(many=True, read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = [
            "id",
            "created_at",
            "status",
            "summary",
            "json_content",
            "formatted_content",
            "categories",
            "size",
        ]
        read_only_fields = ["id", "created_at", "status", "categories", "size"]

    def get_status(self, obj):
        return obj.get_status_display()


class DocumentListSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ["id", "file", "file_type", "status", "created_at", "size"]

    def get_status(self, obj):
        return obj.get_status_display()
