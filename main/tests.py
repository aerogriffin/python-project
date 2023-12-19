from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UserRegistrationTestCase(TestCase):
    def test_user_registration(self):
        registration_url = reverse("register")

        registration_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "testpassword123",
        }
        response = self.client.post(registration_url, registration_data)
        self.assertEqual(response.status_code, 302)
        user_exists = User.objects.filter(username="newuser").exists()
        self.assertTrue(user_exists)

        self.assertTrue("_auth_user_id" in self.client.session)

    def test_user_registration_with_existing_username(self):
        User.objects.create_user(
            username="existinguser",
            email="existinguser@example.com",
            password="password",
        )
        registration_url = reverse("register")
        registration_data = {
            "username": "existinguser",
            "email": "newuser@example.com",
            "password": "password",
        }
        response = self.client.post(registration_url, registration_data)
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertIn("Username is already taken.", form.errors["username"])

    def test_user_registration_with_existing_email(self):
        User.objects.create_user(
            username="existinguser",
            email="existinguser@example.com",
            password="password",
        )
        registration_url = reverse("register")
        registration_data = {
            "username": "newuser",
            "email": "existinguser@example.com",
            "password": "password",
        }
        response = self.client.post(registration_url, registration_data)
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertIn("Email is already in use.", form.errors["email"])

    def test_user_registration_with_invalid_password(self):
        registration_url = reverse("register")
        registration_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "short",
        }
        response = self.client.post(registration_url, registration_data)
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertIn("This password is too short. It must contain at least 8 characters.", form.errors["password"])

    def test_redirect_after_registration(self):
        registration_url = reverse("register")
        registration_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "testpassword123",
        }
        response = self.client.post(registration_url, registration_data)
        self.assertRedirects(response, "/", status_code=302, target_status_code=200)


class UserLoginTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword123",
        )
        self.login_url = reverse("login")

    def test_user_login_success(self):
        login_data = {
            "username": "testuser",
            "password": "testpassword123",
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue("_auth_user_id" in self.client.session)

    def test_user_login_failure(self):
        login_data = {
            "username": "wronguser",
            "password": "testpassword123",
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse("_auth_user_id" in self.client.session)
