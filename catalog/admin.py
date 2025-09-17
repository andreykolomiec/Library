from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from catalog.models import LiteraryFormat, Book, Author

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "price", "format", ]
    list_filter = ["format", ]
    search_fields = ["title", ]


admin.site.register(LiteraryFormat)


@admin.register(Author)
class AuthorAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("pseudonym", )# для відображення полів, які є в класі UserAdmin + поля "pseudonym" в таблиці про авторів
    fieldsets = UserAdmin.fieldsets + (("Additional info", {"fields": ("pseudonym", )}), )# додавання додаткового сігменту "Additional info" з полем "pseudonym" для створення псевдоніму
    add_fieldsets = UserAdmin.add_fieldsets + (("Additional info", {"fields": ("first_name", "last_name", "pseudonym", )}), )# додаемо додаткові поля при створені автора