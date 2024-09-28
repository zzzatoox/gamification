"""
URL configuration for gamification_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from gamification import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('authorization/', views.authorization, name='authorization'),
    path('registration/', views.registration, name='registration'),
    path('create_team/', views.create_team, name='create_team'),
    path('team/', views.team, name='team'),
    path('team/<str:team_id>', views.team, name='team_with_id'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:user_id>', views.profile, name='profile_with_id'),
    path('ratings_teams/', views.ratings_teams, name='ratings_teams'),
    path('ratings_users/', views.ratings_users, name='ratings_users'),
] + static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
