from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UserRegistrationTest(TestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "testpassword123"
        self.email = "test@example.com"
        User.objects.create_user(self.username, self.email, self.password)

    def test_registration_success(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "newpassword123",
            "password2": "newpassword123",
        }
        response = self.client.post(reverse("register"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_registration_with_taken_username(self):
        data = {
            "username": self.username,
            "email": "newuser@example.com",
            "password1": "anotherpassword123",
            "password2": "anotherpassword123",
        }
        response = self.client.post(reverse("register"), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("A user with that username already exists.", response.content.decode())
        self.assertFalse(User.objects.filter(username=data["username"], email="").exists())

    def test_registration_with_taken_email(self):
        data = {
            "username": "anotheruser",
            "password1": "anotherpassword123",
            "password2": "anotherpassword123",
            "email": "test@example.com",
        }
        response = self.client.post(reverse("register"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email=data["email"]).exists())

    def test_user_logout(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
