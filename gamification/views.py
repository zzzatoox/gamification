from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings

from .forms import CreateTaskForm

from django.db import transaction
from .models import (
    User,
    Team,
    TeamEmployee,
    Achievement,
    AchievementEmployee,
    Task,
    TaskEmployee,
    UserProfile,
)


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

        if len(full_name) < 2:
            return render(
                request,
                "account/registration.html",
                {"error_message": "Введите ФИО корректно, каждое слово через пробел"},
            )
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
    return render(request, "account/forgot_password.html", {"form": PasswordResetForm})


@login_required
def get_teams(request):
    user = request.user
    teams = TeamEmployee.objects.filter(employee=user).values_list("team", flat=True)
    teams = Team.objects.filter(id__in=teams)
    return render(request, "teams.html", {"teams": teams})


@login_required
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
    team_list = Team.objects.all().order_by("-xp")

    top_teams = team_list[:3]
    if len(top_teams) == 1:
        top_teams_ordered = [top_teams[0]]
    elif len(top_teams) == 2:
        top_teams_ordered = [top_teams[1], top_teams[0]]
    else:
        top_teams_ordered = [top_teams[1], top_teams[0], top_teams[2]]

    other_teams = team_list[3:]

    return render(
        request,
        "ratings_teams.html",
        {"top_teams": top_teams_ordered, "other_teams": other_teams},
    )


def ratings_users(request):
    user_list = UserProfile.objects.all().order_by("-xp")

    top_users = user_list[:3]
    if len(top_users) == 1:
        top_users_ordered = [top_users[0]]
    elif len(top_users) == 2:
        top_users_ordered = [top_users[1], top_users[0]]
    else:
        top_users_ordered = [top_users[1], top_users[0], top_users[2]]

    other_users = user_list[3:]

    return render(
        request,
        "ratings_users.html",
        {"top_users": top_users_ordered, "other_users": other_users},
    )


@login_required
def team_detail(request, team_id):
    # Проверять, является ли пользователь участником команды и выдавать страницу в зависимости от прав
    user = request.user
    is_team_owner = Team.objects.filter(owner=user, id=team_id).exists()
    is_team_member = TeamEmployee.objects.filter(
        employee=user, team_id=team_id
    ).exists()

    if is_team_owner:
        team = Team.objects.get(id=team_id)
        return render(
            request, "team_detail.html", {"team": team, "is_team_owner": True}
        )
    elif is_team_member:
        team = Team.objects.get(id=team_id)
        return render(
            request, "team_detail.html", {"team": team, "is_team_owner": False}
        )
    else:
        return redirect("home")


@login_required(login_url="authorization")
def team_detail_test(request):
    return render(request, "team_detail_test.html")


def get_user_photo_url(user):
    if user.photo:
        return user.photo.url
    else:
        return settings.STATIC_URL + "images/placeholder.jpg"


def profile(request, user_id):
    user = request.user
    is_user_owner = user.id == user_id

    if is_user_owner:
        user_info = User.objects.get(id=user.id)
        user_game_info = UserProfile.objects.get(user=user_info)
        tasks = TaskEmployee.objects.filter(employee=user_info)
        achievements = AchievementEmployee.objects.filter(employee=user_info)

        return render(
            request,
            "profile.html",
            {
                "user_info": user_info,
                "user_game_info": user_game_info,
                "achievements": achievements,
                "tasks": tasks,
                "is_user_owner": True,
                "user_photo_url": get_user_photo_url(user_info),
            },
        )
    else:
        user_info = User.objects.get(id=user_id)
        user_game_info = UserProfile.objects.get(user=user_info)
        achievements = AchievementEmployee.objects.filter(employee=user_info)

        return render(
            request,
            "profile.html",
            {
                "user_info": user_info,
                "user_game_info": user_game_info,
                "achievements": achievements,
                "is_user_owner": False,
                "user_photo_url": get_user_photo_url(user_info),
            },
        )


@login_required
def create_task(request):
    if request.method == "POST":
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = CreateTaskForm()

    return render(request, "create_task.html", {"form": form})


@login_required
def complete_task(request, task_id, employee_id):
    task_employee = get_object_or_404(
        TaskEmployee, task_id=task_id, employee_id=employee_id
    )

    if task_employee.completed_at:
        messages.error(request, "Задача уже выполнена")
        return redirect("task_detail", task_id=task_id)

    task_employee.completed_at = timezone.now()
    task_employee.save()

    user = task_employee.employee
    user.xp += task_employee.task.xp_reward
    user.save()

    messages.success(request, "Задача выполнена")
    return redirect("task_detail", task_id=task_id)
