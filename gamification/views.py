from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect, render
from django.contrib.auth.models import User


# Create your views here.
def home(request):
    return render(request, "home.html")


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("home")
        else:
            return render(
                request,
                "authorization.html",
                {"error_message": "Неверные учетные данные"},
            )
    else:
        return render(request, "login.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        repeat_password = request.POST["repeat_password"]
        full_name = request.POST["full_name"]

        # Normalize full_name
        full_name = full_name.strip().split()
        last_name = full_name[0]
        first_name = full_name[1]
        patronymic = full_name[-1] if len(full_name) > 1 else ""

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "registration.html",
                {"error_message": "Имя пользователя уже существует"},
            )
        elif User.objects.filter(email=email).exists():
            return render(
                request,
                "registration.html",
                {"error_message": "Email уже зарегистрирован"},
            )
        elif password != repeat_password:
            return render(
                request, "registration.html", {"error_message": "Пароли не совпадают"}
            )
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                last_name=last_name,
                first_name=first_name,
                patronymic=patronymic,
            )
            auth_login(request, user)
            return redirect("home")
    else:
        return render(request, "register.html")
