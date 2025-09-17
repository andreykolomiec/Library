from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from catalog.models import LiteraryFormat

LITERARY_FORMAT_URL = reverse("catalog:literary-format-list")

class PublicLiteraryFormatTest(TestCase):
    # def setUp(self) -> None:
    #     self.client = Client()  # Цей обєкт client Django по дефолту робить за нас, тобто,
    #     # якщо ми не хочемо тут зробити зробити логін юзера або зробити Client() дещо іншим,
    #     # ми можемо його явно не ініціалізувати, а використати вбудований функціонал

    def test_login_required(self):
        res = self.client.get(LITERARY_FORMAT_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateLiteraryFormatTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_literary_formats(self):
        LiteraryFormat.objects.create(name="test_format1")
        LiteraryFormat.objects.create(name="test_format2")
        response = self.client.get(LITERARY_FORMAT_URL)
        self.assertEqual(response.status_code, 200) # перевіряємо статус-код запиту (get): чи буде запит дорівнювати 200

        literary_format11 = LiteraryFormat.objects.all() # створюємо змінну, в яку вписуємо всі літературні форматих
        self.assertEqual(
            list(response.context["key_literary_formats_list"]),
            list(literary_format11),
        )# чи містяться в контексті для view відповідні обєкти, які ми тестуємо

        self.assertTemplateUsed(
            response,
            "catalog/literary_format_list.html"
        ) #чи використовується корректний темплейт для нашого view
