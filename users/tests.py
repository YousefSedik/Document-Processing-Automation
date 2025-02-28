from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from faker import Faker
from users.models import User


class UserRegisterTests(APITestCase):

    def test_create_user(self):
        fake = Faker()
        e, p = fake.email(), fake.password()
        self.data = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": e,
            "password": p,
            "password2": p,
        }
        url = reverse("users:create_user")
        response = self.client.post(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, self.data["email"].lower())
        # try to create a user with the same email
        response = self.client.post(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)


class UserLoginTest(APITestCase):
    def setUp(self):
        # create a user
        fake = Faker()
        e, p = fake.email(), fake.password()
        self.data = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": e,
            "password": p,
            "password2": p,
        }

        register_url = reverse("users:create_user")
        self.client.post(register_url, self.data, format="json")
        self.assertEqual(User.objects.count(), 1)

    def test_login(self):
        url = reverse("users:token_obtain_pair")
        login_data = {
            "email": self.data["email"],
            "password": self.data["password"],
        }
        response = self.client.post(url, login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        # try to login with wrong email
        response = self.client.post(
            url, {"email": "gg@gg.com", "password": "1234"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # try to login with wrong password
        response = self.client.post(
            url, {"email": self.data["email"], "password": "1234"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
