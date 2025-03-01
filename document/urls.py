from django.urls import path
from document.api import (
    DocumentCreateView,
    DocumentListView,
    DocumentRetrieveUpdateDestroyView,
)

app_name = "document"
urlpatterns = [
    path("document/", DocumentCreateView.as_view(), name="create-document"),
    path("documents/", DocumentListView.as_view(), name="document-list"),
    path(
        "document/<int:id>/",
        DocumentRetrieveUpdateDestroyView.as_view(),
        name="document-retrieve-update-destroy",
    ),
]
