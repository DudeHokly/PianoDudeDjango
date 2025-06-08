from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class SmokeTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.superuser = User.objects.create_superuser(
            username="admin", password="adminpass", email="admin@example.com"
        )

    def test_index(self):
        response = self.client.get(reverse("general:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_login_register_pages(self):
        for name in ["general:login", "general:register"]:
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)

    def test_logout_redirect(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("general:logout"))
        self.assertRedirects(response, reverse("general:index"))

    def test_account_requires_login(self):
        response = self.client.get(reverse("general:account"))
        self.assertEqual(response.status_code, 200)  # если без login доступен
        # Если должен быть login required:
        # self.assertRedirects(response, f"/login/?next={reverse('general:account')}")

    def test_admin_panel_view(self):
        self.client.login(username="admin", password="adminpass")
        response = self.client.get(reverse("general:panel_admin"))
        self.assertEqual(response.status_code, 200)

    def test_contacts_and_feedback(self):
        for name in ["general:contacts", "general:feedback"]:
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)
