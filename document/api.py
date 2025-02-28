from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Document
from .serializers import DocumentSerializer


class DocumentCreateView(CreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
