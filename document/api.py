from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from .models import Document
from .serializers import DocumentCreateSerializer, DocumentRetrieveSerializer


class DocumentCreateView(CreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DocumentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentRetrieveSerializer
    lookup_field = "id"

    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)


class DocumentListView(ListAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentRetrieveSerializer

    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)
