from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="test_admin",
        )
        self.client.force_login(self.admin_user)
        self.author = get_user_model().objects.create_user(
            username="author",
            password="test_author",
            pseudonym="test pseudonym",
        )

    def test_author_pseudonym_listed(self):
        """
        Test that authors pseudonym is in list_display on author admin page.
        :return:
        """

        url = reverse("admin:catalog_author_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.author.pseudonym)

    def test_author_detail_pseudonym_listed(self):
        """
        Test that authors pseudonym is on author detail admin page.
        :return:
        """
        url = reverse("admin:catalog_author_change", args=[self.author.id])
        res = self.client.get(url)
        self.assertContains(res, self.author.pseudonym)

    def test_author_additional_info(self):
        """
        Test that author page contains the correct fields.
        :return:
        """
        url = reverse("admin:catalog_author_add")
        res = self.client.get(url)
        self.assertContains(res, "First name")
        self.assertContains(res, "Last name")
        self.assertContains(res, "Pseudonym")
