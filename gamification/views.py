from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect, render
from .models import User, Team, TeamEmployee
from django.contrib.auth.forms import PasswordResetForm


# Create your views here.
def home(request):
    return render(request, "home.html")


def authorization(request):
    if request.method == "POST":
        login_or_email = request.POST.get("login_or_email")
        password = request.POST.get("password")

        # Проеверяем логин или email
        if "@" in login_or_email:
            UserModel = get_user_model()
            try:
                user = UserModel.objects.get(email=login_or_email)
                if user.check_password(password):
                    auth_login(request, user)
                    return redirect("home")
                else:
                    print("Неверный пароль для электронной почты")
            except UserModel.DoesNotExist:
                print("Пользователь с таким электронным адресом не существует")
        else:
            user = authenticate(request, username=login_or_email, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("home")
        else:
            return render(
                request,
                "account/authorization.html",
                {"error_message": "Неверный логин или пароль"},
            )
    else:
        return render(request, "account/authorization.html")


def registration(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        repeat_password = request.POST.get("repeat_password")
        full_name = request.POST.get("full_name")

        # Проверка на наличие символа @ в логине
        if "@" in username:
            return render(
                request,
                "account/registration.html",
                {"error_message": "Логин не может содержать символ '@'"},
            )
        
        full_name = full_name.strip().split()

        if len(full_name)<2:
            return render(request,
                          'account/registration.html',
                          {'error_message':"Введите ФИО корректно, каждое слово через пробел"})
        full_name = [name.capitalize() for name in full_name]
        last_name = full_name[0]
        first_name = full_name[1]
        patronymic = full_name[-1] if len(full_name) > 1 else ""

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "account/registration.html",
                {"error_message": "Имя пользователя уже существует"},
            )
        elif User.objects.filter(email=email).exists():
            return render(
                request,
                "account/registration.html",
                {"error_message": "Email уже зарегистрирован"},
            )
        elif password != repeat_password:
            return render(
                request,
                "account/registration.html",
                {"error_message": "Пароли не совпадают"},
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
        return render(request, "account/registration.html")


def logout(request):
    auth_logout(request)
    return redirect("home")

def forgot_password(request):
    return render(request, 'account/forgot_password.html', {'form':PasswordResetForm})


@login_required(login_url='authorization')
def create_team(request):
    if request.method == "POST":
        title = request.POST.get("title")
        photo = request.FILES.get("photo")
        owner = request.user

        team = Team.objects.create(owner=owner, title=title, photo=photo)
        TeamEmployee.objects.create(team=team, employee=owner)
        return redirect("team")
    return render(request, "create_team.html")


def ratings_teams(request):
    return render(request, "ratings_teams.html")


def ratings_users(request):
    return render(request, "ratings_users.html")


def teams(request):
    team_list = Team.objects.get().order_by('xp')
    return render(request, 'teams.html', context=team_list)

@login_required(login_url='authorization')
def team_detail(request):
    # Проверять, является ли пользователь участником команды и выдавать страницу в зависимости от прав
    user = request.user
    is_team_owner = Team.objects.filter(owner=user).exists()
    is_team_member = TeamEmployee.objects.filter(employee=user).exists()

    if is_team_owner:
        pass #context add
    elif is_team_member:
        pass#context add
    return render(request, "team_details.html")

@login_required(login_url='authorization')
def team_detail_test(request):
    return render(request, 'team_detail_test.html')

def profile(request):
    # Проверять, является ли пользователь владельцем своей страницы, и выдавать соотв. функционал

    return render(request, "profile.html")
