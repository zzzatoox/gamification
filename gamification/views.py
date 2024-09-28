from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def authorization(request):
    return render(request, 'authorization.html')

def registration(request):
    return render(request, 'registration.html')

def create_team(request):
    return render(request, 'create_team.html')

def ratings_teams(request):
    return render(request, 'ratings_teams.html')

def ratings_users(request):
    return render(request, 'ratings_users.html')

def team(request):
    # Проверять, является ли пользователь участником команды и выдавать страницу в зависимости от прав
    return render(request, 'team.html')

def profile(request):
    # Проверять, является ли пользователь владельцем своей страницы, и выдавать соотв. функционал
    return render(request, 'profile.html')

