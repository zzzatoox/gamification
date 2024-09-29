from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("authorization/", views.authorization, name="authorization"),
    path("registration/", views.registration, name="registration"),
    path("logout/", views.logout, name="logout"),
    path("create_team/", views.create_team, name="create_team"),
    path("team/", views.team, name="team"),
    path("team/<int:team_id>", views.team, name="team_with_id"),
    path("profile/", views.profile, name="profile"),
    path("profile/<int:user_id>", views.profile, name="profile_with_id"),
    path("ratings_teams/", views.ratings_teams, name="ratings_teams"),
    path("ratings_users/", views.ratings_users, name="ratings_users"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
