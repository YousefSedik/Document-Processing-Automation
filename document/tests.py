from rest_framework.test import APITestCase
from .models import Document
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from faker import Faker
from rest_framework import status

User = get_user_model()


class CreateDocumentTestCase(APITestCase):

    def setUp(self):
        """
        Create a user and store the email and password in self.e and self.p
        """
        f = Faker()
        self.e, self.p = f.email(), f.password()
        self.user = User.objects.create_user(email=self.e, password=self.p)
        return super().setUp()

    def test_create_document_without_logged_in_user(self):
        """
        Test that a document cannot be created without a logged in user.
        this test should return a 401 status code.
        """
        data = {
            "file": SimpleUploadedFile("test.pdf", b"file_content"),
        }
        create_url = reverse("document:create-document")
        response = self.client.post(create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Document.objects.count(), 0)

    def test_create_document_with_logged_in_user(self):
        """
        Test that a document can be created with a logged in user.
        this test should return a 201 status code.
        """
        self.client.login(username=self.e, password=self.p)
        data = {
            "file": SimpleUploadedFile("test.pdf", b"file_content"),
        }
        create_url = reverse("document:create-document")
        response = self.client.post(create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Document.objects.count(), 1)

    def test_create_document_with_valid_file_types(self):
        """
        Test that a document can be created with valid file types (pdf, png, jpg, jpeg).
        this test should return a 201 status code.
        """
        self.client.login(username=self.e, password=self.p)
        create_url = reverse("document:create-document")
        allowed_file_types = [".pdf", ".png", ".jpg", ".jpeg"]
        for i, format in enumerate(allowed_file_types):
            data = {
                "file": SimpleUploadedFile(f"test.{format}", b"file_content"),
            }
            response = self.client.post(create_url, data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Document.objects.count(), i + 1)

    def test_create_document_with_invalid_file_extension(self):
        """
        Test that a document cannot be
        created with an invalid file extension.
        this test should return a 400 status code.
        """
        self.client.login(username=self.e, password=self.p)
        data = {
            "file": SimpleUploadedFile("test.txt", b"file_content"),
        }
        create_url = reverse("document:create-document")
        response = self.client.post(create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Document.objects.count(), 0)

    def test_create_document_with_invalid_file_size(self):
        """
        Test that a document cannot be
        created with an invalid file size.
        this test should return a 400 status code.
        """
        self.client.login(username=self.e, password=self.p)
        data = {
            "file": SimpleUploadedFile("test.pdf", b"file_content" * 1024 * 1024 * 101),
        }
        create_url = reverse("document:create-document")
        response = self.client.post(create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Document.objects.count(), 0)


class ViewDocumentTestCase(APITestCase):
    def setUp(self):
        """
        Create a user and store the email and password in self.e and self.p
        Ceate a document and store the document in self.document
        """
        f = Faker()
        self.e, self.p = f.email(), f.password()
        self.user = User.objects.create_user(email=self.e, password=self.p)
        # other user
        user2 = User.objects.create_user(email="ee@g.com", password="fhhu1232@@X")
        self.document_user_1 = Document.objects.create(
            file=SimpleUploadedFile("test.pdf", b"file_content"), user=self.user
        )
        self.document_user_2 = Document.objects.create(
            file=SimpleUploadedFile("test.png", b"file_content"), user=user2
        )

        return super().setUp()

    def test_list_document(self):
        """
        Test that a document can be listed.
        this test should return a 200 status code.
        """
        self.client.login(username=self.e, password=self.p)
        list_url = reverse("document:document-list")
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_owned_document(self):
        """
        Test that a document can be retrieved.
        this test should return a 200 status code.
        """
        self.client.login(username=self.e, password=self.p)
        retrieve_url = reverse(
            "document:document-retrieve-update-destroy", args=[self.document_user_1.id]
        )
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"), self.document_user_1.id)

    def test_unauthorized_retrieve_document(self):
        """
        Test that a document cannot be retrieved without a logged in user.
        this test should return a 401 status code.
        """
        retrieve_url = reverse(
            "document:document-retrieve-update-destroy", args=[self.document_user_1.id]
        )

        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_list_document(self):
        """
        Test that a document cannot be listed without a logged in user.
        this test should return a 401 status code.
        """
        list_url = reverse("document:document-list")
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_retrieve_other_user_document(self):
        """
        Test that a document cannot be retrieved by another user.
        this test should return a 404 status code.
        """
        self.client.login(username=self.e, password=self.p)
        retrieve_url = reverse(
            "document:document-retrieve-update-destroy", args=[self.document_user_2.id]
        )
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
