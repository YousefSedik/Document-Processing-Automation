from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from .models import Document
from .serializers import (
    DocumentCreateSerializer,
    DocumentRetrieveUpdateDestroySerializer,
    DocumentListSerializer,
)
from .permissions import DocumentPermission
from rest_framework.permissions import IsAuthenticated
from django.http import Http404

class DocumentCreateView(CreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DocumentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentRetrieveUpdateDestroySerializer
    permission_classes = [IsAuthenticated, DocumentPermission]
    lookup_field = "id"

    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise Http404  # Return 404 if the user does not own the document
        return obj


class DocumentListView(ListAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentListSerializer

    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)
