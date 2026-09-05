from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthenticationTests(APITestCase):

    def setUp(self):
        self.register_url = "/api/auth/register/"
        self.login_url = "/api/auth/login/"
        self.profile_url = "/api/auth/profile/"
        self.change_password_url = "/api/auth/change-password/"

        self.user_data = {
            "username": "sammy",
            "email": "sammy@example.com",
            "password": "password123",
        }

    def test_registration(self):
        response = self.client.post(
            self.register_url,
            self.user_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            User.objects.filter(
                email="sammy@example.com"
            ).exists()
        )

        # Password must not appear in the response
        self.assertNotIn("password", response.data)

    def test_login(self):
        User.objects.create_user(
            username="sammy",
            email="sammy@example.com",
            password="password123"
        )

        response = self.client.post(
            self.login_url,
            {
                "email": "sammy@example.com",
                "password": "password123",
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_invalid_password(self):
        User.objects.create_user(
            username="sammy",
            email="sammy@example.com",
            password="password123"
        )

        response = self.client.post(
            self.login_url,
            {
                "email": "sammy@example.com",
                "password": "wrongpassword",
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_unauthenticated_profile(self):
        response = self.client.get(self.profile_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_authenticated_profile(self):
        user = User.objects.create_user(
            username="sammy",
            email="sammy@example.com",
            password="password123"
        )

        self.client.force_authenticate(user=user)

        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "sammy@example.com")

    def test_update_profile(self):
        user = User.objects.create_user(
            username="sammy",
            email="sammy@example.com",
            password="password123"
        )

        self.client.force_authenticate(user=user)

        response = self.client.patch(
            self.profile_url,
            {
                "first_name": "Sammy",
                "last_name": "Njuguna",
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user.refresh_from_db()

        self.assertEqual(user.first_name, "Sammy")
        self.assertEqual(user.last_name, "Njuguna")

    def test_change_password(self):
        user = User.objects.create_user(
            username="sammy",
            email="sammy@example.com",
            password="password123"
        )

        self.client.force_authenticate(user=user)

        response = self.client.post(
            self.change_password_url,
            {
                "old_password": "password123",
                "new_password": "newpassword123",
                "new_password_confirm": "newpassword123",
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user.refresh_from_db()

        self.assertTrue(
            user.check_password("newpassword123")
        )
