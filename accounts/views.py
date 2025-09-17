from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request, "registration/login.html")
    elif request.method == "POST":
        username1 = request.POST["username"]
        password1 = request.POST["password"]
        user = authenticate(username=username1, password=password1)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("catalog:index"))# тут при залогинені Django перенаправляє користувача
                                                                # на головну сторінку сайту ("catalog:index")
        else:
            error_context = {
                "error": "Invalid credentials.",
            }
            return render(request, "registration/login.html", context=error_context)

#
# def logout_view(request: HttpRequest) -> HttpResponse:
#     logout(request)
#     return render(request, "registration/logged_out.html")