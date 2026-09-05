from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class AuthenticationTests(APITestCase):

    def setUp(self):
        self.register_url = reverse("register")
        self.login_url = reverse("token_obtain_pair")
        self.profile_url = reverse("profile")
        self.change_password_url = reverse("change-password")

        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "StrongPass123",
        }

    def test_user_registration(self):
        response = self.client.post(
            self.register_url,
            self.user_data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            User.objects.filter(
                email="test@example.com"
            ).exists()
        )

    def test_jwt_login(self):
        User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="StrongPass123",
        )

        response = self.client.post(
            self.login_url,
            {
                "email": "test@example.com",
                "password": "StrongPass123",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_profile_requires_authentication(self):
        response = self.client.get(self.profile_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_authenticated_profile(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="StrongPass123",
        )

        self.client.force_authenticate(user=user)

        response = self.client.get(self.profile_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["email"],
            "test@example.com",
        )


    def test_profile_update(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="StrongPass123",
        )

        self.client.force_authenticate(user=user)

        response = self.client.patch(
            self.profile_url,
            {
                "first_name": "Updated",
                "last_name": "Name",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        user.refresh_from_db()

        self.assertEqual(user.first_name, "Updated")
        self.assertEqual(user.last_name, "Name")

    def test_change_password(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="StrongPass123",
        )

        self.client.force_authenticate(user=user)

        response = self.client.post(
            self.change_password_url,
            {
                "old_password": "StrongPass123",
                "new_password": "NewStrongPass123",
                "new_password_confirm": "NewStrongPass123",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        user.refresh_from_db()

        self.assertTrue(
            user.check_password("NewStrongPass123")
        )
