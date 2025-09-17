import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import AuthorCreationForm, BookForm, BookSearchForm
from .models import Book, Author, LiteraryFormat


@login_required# цей декоратор забороняє потрапляти на головну сторінку (Home) не залогіненим користувачам, але він працює лише з FBV (function base view)
def index(request: HttpRequest) -> HttpResponse:
    # now = datetime.datetime.now()
    #print(f"Request params: {request.GET}")
    num_books = Book.objects.all().count()
    num_authors = Author.objects.count()
    num_literary_formats = LiteraryFormat.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {
        'key_num_books': num_books,
        "key_num_authors": num_authors,
        "key_num_literary_formats": num_literary_formats,
        "num_visits": num_visits + 1,
    }
    return render(
        request,
        "catalog/index.html",
        context=context
    )



# def literary_format_list_view(request: HttpRequest) -> HttpResponse:
#     literary_formats_list = LiteraryFormat.objects.all()
#     context = {
#         'key_literary_formats_list': literary_formats_list,
#     }
#     return render(
#         request,
#         "catalog/literary_format_list.html",
#         context=context
#     )


class LiteraryFormatListView(LoginRequiredMixin, generic.ListView):# для заборони потрапляння не залогіненим користувачам в CBV (Class Base View) використовуються міксини
    model = LiteraryFormat
    template_name = "catalog/literary_format_list.html"
    context_object_name = "key_literary_formats_list"
    paginate_by = 4


class LiteraryFormatCreateView(LoginRequiredMixin, generic.CreateView):
    model = LiteraryFormat
    fields = "__all__"
    success_url = reverse_lazy("catalog:literary-format-list")# на цю адресу користувача буде редіректити після заповнення форми
    template_name = "catalog/literary_format_form.html"# в цьому випадку (при створенні) форма для заповнення буде пуста


class LiteraryFormatUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = LiteraryFormat
    fields = "__all__"
    success_url = reverse_lazy("catalog:literary-format-list")#на цю адресу користувача буде редіректити після заповнення форми
    template_name = "catalog/literary_format_form.html"# в цьому випадку (при оновленні) форма буде вже заповнена


class LiteraryFormatDeleteView(LoginRequiredMixin,generic.DeleteView):
    model = LiteraryFormat
    template_name = "catalog/literary_format_confirm_delete.html"
    success_url = reverse_lazy("catalog:literary-format-list")


class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    # queryset = Book.objects.select_related("format")
    paginate_by = 2

    # додаємо опцію, щоб введений текст зберігався. Для цього треба змінити метод:
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        context["search_form"] = BookSearchForm(
            initial={"title": title},
        )
        return context

    # # реалізуємо пошук за допомогою пошукового слова title. Для цього треба змінити метод:
    # def get_queryset(self):
    #     title = self.request.GET.get("title", "")
    #     if title:
    #         return self.queryset.filter(title__icontains=title)
    #     return self.queryset


# реалізуємо пошук за допомогою створеною нами форми BookSearchForm. Для цього треба змінити метод:
    def get_queryset(self):
        queryset = Book.objects.select_related("format")
        form = BookSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(title__icontains=form.cleaned_data["title"])
        return queryset


class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    paginate_by = 3


# def book_detail_view(request: HttpRequest, pk: int) -> HttpResponse:
#     try:
#         book = Book.objects.get(id=pk)
#     except Book.DoesNotExist:
#         raise Http404("Book does not exist")
#
#     context = {
#         "key_book": book,
#     }
#     return render(request, "catalog/book_detail.html", context=context)


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book


class BookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Book
    # fields = "__all__"
    form_class = BookForm


class BookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Book
    form_class = BookForm


class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author


class AuthorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Author
    form_class = AuthorCreationForm
    # template_name = "catalog/author_form.html"




# def test_session_view(request: HttpRequest) -> HttpResponse:
#     return HttpResponse(
#         "<h1>Test Session</h1>"
#         f"<h4>Session Data: {request.session['book']}</h4>"
#     )


