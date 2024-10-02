from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.db.models import Q

from .forms import TaskForm, RegistrationForm, TeamForm

from django.http import JsonResponse

from django.db import transaction
from .models import (
    User,
    Team,
    TeamEmployee,
    AchievementEmployee,
    Task,
    TaskEmployee,
    UserProfile,
    Status,
    Product,
)

CREATED_STATUS = Status.objects.get_or_create(title="Создана")[0]
IN_PROGRESS_STATUS = Status.objects.get_or_create(title="В процессе")[0]
ON_TEST_STATUS = Status.objects.get_or_create(title="На проверке")[0]
COMPLETED_STATUS = Status.objects.get_or_create(title="Выполнена")[0]


# Create your views here.
def home(request):
    return render(request, "home.html")


def authorization(request):
    if request.method == "POST":
        login_or_email = request.POST.get("login_or_email")
        password = request.POST.get("password")

        UserModel = get_user_model()
        try:
            if "@" in login_or_email:
                user = UserModel.objects.get(email=login_or_email)
            else:
                user = UserModel.objects.get(username=login_or_email)

            if user.check_password(password):
                auth_login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Неверный логин или пароль")
        except UserModel.DoesNotExist:
            messages.error(request, "Пользователь не найден")
        else:
            user = authenticate(request, username=login_or_email, password=password)

        return render(request, "account/authorization.html")
    else:
        return render(request, "account/authorization.html")


def registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("home")
    else:
        form = RegistrationForm()
    return render(request, "account/registration.html", {"form": form})


def logout(request):
    auth_logout(request)
    return redirect("home")


def forgot_password(request):
    return render(request, "account/forgot_password.html", {"form": PasswordResetForm})


@login_required
def get_teams(request):
    user = request.user
    owned_teams = Team.objects.filter(owner=user)
    member_teams = TeamEmployee.objects.filter(employee=user).exclude(team__owner=user)

    # получаем фотографии
    owned_teams_with_photos = [
        {"team": team, "photo_url": get_team_photo_url(team)} for team in owned_teams
    ]

    member_teams_with_photos = [
        {
            "team": team_employee.team,
            "photo_url": get_team_photo_url(team_employee.team),
        }
        for team_employee in member_teams
    ]

    return render(
        request,
        "teams.html",
        {
            "owned_teams": owned_teams_with_photos,
            "member_teams": member_teams_with_photos,
        },
    )


@login_required
def create_team(request):
    if request.method == "POST":
        form = TeamForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                team = form.save(commit=False)
                team.owner = request.user
                team.save()
                TeamEmployee.objects.create(team=team, employee=request.user)
            return redirect("teams")
    else:
        form = TeamForm()
    return render(request, "create_team.html", {"form": form})


@login_required
def edit_team(request):
    if request.method == "POST":
        team = get_object_or_404(Team, team_id=request.POST.get("team_id"))
        team.title = request.POST.get("title")
        if "photo" in request.FILES:
            team.photo = request.FILES["photo"]
        team.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "message": "Invalid request method"})


def ratings_teams(request):
    team_list = Team.objects.all().order_by("-xp")
    if team_list.count() > 0:
        top_teams = team_list[:3]

        if len(top_teams) == 1:
            top_teams_ordered = [top_teams[0]]
        elif len(top_teams) == 2:
            top_teams_ordered = [top_teams[1], top_teams[0]]
        else:
            top_teams_ordered = [top_teams[1], top_teams[0], top_teams[2]]

        other_teams = team_list[3:]

        # получаем фотографии
        top_teams_with_photos = [
            {"team": team, "photo_url": get_team_photo_url(team)}
            for team in top_teams_ordered
        ]

        other_teams_with_photos = [
            {"team": team, "photo_url": get_team_photo_url(team)}
            for team in other_teams
        ]

        return render(
            request,
            "ratings_teams.html",
            {
                "top_teams": top_teams_with_photos,
                "other_teams": other_teams_with_photos,
            },
        )
    return render(request, "ratings_teams.html")


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

    # получаем фотографии
    top_teams_with_photos = [
        {"user": user, "photo_url": get_user_photo_url(user.user)}
        for user in top_users_ordered
    ]

    other_teams_with_photos = [
        {"user": user, "photo_url": get_user_photo_url(user.user)}
        for user in other_users
    ]

    return render(
        request,
        "ratings_users.html",
        {"top_users": top_teams_with_photos, "other_users": other_teams_with_photos},
    )


@login_required(login_url="authorization")
def team_detail_test(request, team_id):
    # участники команды
    team = Team.objects.get(team_id=team_id)
    members = team.members.all()
    member_photos = [get_user_photo_url(member.employee) for member in members]
    members_with_photos = list(zip(members, member_photos))

    # получение задач
    tasks = Task.objects.filter(team=team)

    waiting_tasks = tasks.filter(status=CREATED_STATUS)
    in_progress_tasks = tasks.filter(status=IN_PROGRESS_STATUS)

    seven_days_ago = timezone.now() - timezone.timedelta(days=7)
    completed_tasks = tasks.filter(
        Q(assignments__completed_at__gte=seven_days_ago) | Q(status=ON_TEST_STATUS)
    ).distinct()

    return render(
        request,
        "team_detail_test.html",
        {
            "team": team,
            "team_photo_url": get_team_photo_url(team),
            "members": members_with_photos,
            "waiting_tasks": waiting_tasks,
            "in_progress_tasks": in_progress_tasks,
            "completed_tasks": completed_tasks,
        },
    )


@login_required(login_url="authorization")
def invite_in_team(request):  #  (request, team_id)
    # все пользователи
    all_users = User.objects.exclude(is_superuser=True)
    all_users_photos = [get_user_photo_url(user) for user in all_users]
    all_users_with_photos = list(zip(all_users, all_users_photos))

    return render(
        request,
        "invite.html",
        {
            "all_users_with_photos": all_users_with_photos,
        },
    )


@login_required(login_url="authorization")
def shop(request):
    products = Product.objects.all()
    return render(
        request,
        "shop.html",
        {"products": products},
    )


@login_required(login_url="authorization")
def buy_product(request): ...


def get_user_photo_url(user):
    if user.photo:
        return user.photo.url
    else:
        return settings.STATIC_URL + "images/placeholder_profile.jpg"


def get_team_photo_url(team):
    if team.photo:
        return team.photo.url
    else:
        return settings.STATIC_URL + "images/placeholder_team.jpg"


def profile(request, user_id):
    user = request.user
    is_user_owner = user.id == user_id

    user_info = get_object_or_404(User, id=user_id)
    user_game_info = get_object_or_404(UserProfile, user=user_info)
    achievements = AchievementEmployee.objects.filter(employee=user_info)

    context = {
        "user_info": user_info,
        "user_game_info": user_game_info,
        "achievements": achievements,
        "is_user_owner": is_user_owner,
        "user_photo_url": get_user_photo_url(user_info),
    }

    if is_user_owner:
        tasks = TaskEmployee.objects.filter(
            employee=user_info, status=IN_PROGRESS_STATUS
        )
        context["tasks"] = tasks

    return render(request, "profile.html", context)


@login_required
def create_task(request):
    if request.method == "POST":
        with transaction.atomic():
            title = request.POST.get("title")
            description = request.POST.get("description")
            team_id = request.POST.get("team_id")

            team = Team.objects.get(team_id=team_id)

            Task.objects.create(
                title=title,
                description=description,
                team=team,
                xp_reward=10,  # TODO: подставить реальное значение
                coins_reward=5,  # TODO: подставить реальное значение
                status=CREATED_STATUS,
            )

            return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Invalid request method"})


@login_required
def take_task(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Task, task_id=task_id)
        user = request.user

        # Проверка, что задача еще не взята другим пользователем
        if TaskEmployee.objects.filter(task=task).exists():
            return JsonResponse(
                {"success": False, "message": "Задача уже взята другим пользователем."}
            )

        with transaction.atomic():
            # Создаем запись о том, что задача взята пользователем
            TaskEmployee.objects.create(
                task=task, employee=user, status=Status.objects.get(title="В процессе")
            )

            # Обновляем статус задачи
            task.status = Status.objects.get(title="В процессе")
            task.save()

            return JsonResponse({"success": True, "message": "Задача успешно взята."})
    return JsonResponse({"success": False, "error": "Invalid request method"})


@login_required
def assign_task(request):
    if request.method == "POST":
        with transaction.atomic():
            task_id = request.POST.get("task_id")
            executor_id = request.POST.get("executor")

            task_employee = get_object_or_404(
                TaskEmployee, task_id=task_id, employee_id=executor_id
            )
            task = task_employee.task

            task_employee.status = IN_PROGRESS_STATUS
            task_employee.save()

            task.status = IN_PROGRESS_STATUS
            task.save()

            return JsonResponse({"success": True})
    return JsonResponse({"success": False, "error": "Invalid request method"})


@login_required
def submit_task(request):
    if request.method == "POST":
        with transaction.atomic():
            task_id = request.POST.get("task_id")
            employee_id = request.POST.get("employee_id")

            task_employee = get_object_or_404(
                TaskEmployee, task_id=task_id, employee_id=employee_id
            )
            task = task_employee.task

            task.status = ON_TEST_STATUS
            task.save()

            task_employee.status = ON_TEST_STATUS
            task_employee.save()

            return JsonResponse({"success": True})
    return JsonResponse({"success": False, "error": "Invalid request method"})


@login_required
def complete_task(request):
    if request.method == "POST":
        with transaction.atomic():
            task_id = request.POST.get("task_id")
            employee_id = request.POST.get("employee_id")

            # получаю объект задачи и связи
            task_employee = get_object_or_404(
                TaskEmployee, task_id=task_id, employee_id=employee_id
            )
            task = task_employee.task

            # изменяю статус задачи и связи
            task_employee.status = COMPLETED_STATUS
            task_employee.completed_at = timezone.now()
            task_employee.save()

            task.status = COMPLETED_STATUS
            task.save()

            # получаю объект профиля пользователя
            employee_profile = UserProfile.objects.get(user=task_employee.employee)

            # изменяю количество опыта и монет
            employee_profile.complete_task(task.xp_reward, task.coins_reward)

            return JsonResponse({"success": True})
    return JsonResponse({"success": False, "error": "Invalid request method"})
