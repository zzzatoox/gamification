from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


class AuthorizationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_valid_login_redirects_to_home(self):
        response = self.client.post(
            reverse("authorization"),
            {"login_or_email": "testuser", "password": "testpassword"},
        )
        self.assertRedirects(response, reverse("home"))

    def test_invalid_login_and_password_displays_error_message(self):
        response = self.client.post(
            reverse("authorization"),
            {"login_or_email": "invalid_user", "password": "invalid_password"},
        )
        self.assertContains(response, "Неверный логин или пароль")
