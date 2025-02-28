from django.urls import path
from document.api import DocumentCreateView

urlpatterns = [
    path("document/", DocumentCreateView.as_view(), name="document-list-create"),
]
