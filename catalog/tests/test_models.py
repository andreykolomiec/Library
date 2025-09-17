from django.contrib.auth import get_user_model
from django.test import TestCase

from catalog.models import LiteraryFormat, Author, Book


class ModelTest(TestCase):
    def test_literaryformat_str(self):
        literary_format = LiteraryFormat.objects.create(name='test')
        self.assertEqual(str(literary_format), literary_format.name)

    def test_author_str(self):
        author = get_user_model().objects.create(
            username='user_test',
            password="test_password",
            first_name='first_name_test',
            last_name='last_name_test',
        )
        self.assertEqual(str(author), f"{author.username}: {author.first_name} {author.last_name}")

    def test_book_str(self):
        literary_format = LiteraryFormat.objects.create(name='test_literary_format')
        book = Book.objects.create(title='test_book_title', price='10.11', format=literary_format)
        self.assertEqual(str(book), f"{book.title} (price: {book.price}), format: {book.format.name}")

    def test_create_author_with_pseudonym(self):
        username1 = 'user_test'
        password1 = "test_password"
        pseudonym1 = 'pseudonym_test'
    # тут при створені author використовуємо create_user замість create, для того, щоб захешувати password1
        author = get_user_model().objects.create_user(
            username=username1,
            password=password1,
            pseudonym=pseudonym1,
        )
        self.assertEqual(author.username, username1)
        self.assertEqual(author.pseudonym, pseudonym1)
    # перевіряємо на відповідність паролів за доп assertTrue та захешованого пароля за доп методу check_password()
        self.assertTrue(author.check_password(password1))
