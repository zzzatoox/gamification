from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("authorization/", views.authorization, name="authorization"),
    path("registration/", views.registration, name="registration"),
    path("forgot_password/", views.forgot_password, name="forgot_password"),
    path("logout/", views.logout, name="logout"),
    path("create_team/", views.create_team, name="create_team"),
    path("teams/", views.get_teams, name="teams"),
    path("team_detail/<int:team_id>/", views.team_detail_test, name="team_detail"),
    path("edit_team/", views.edit_team, name="edit_team"),
    path("create_task/", views.create_task, name="create_task"),
    path("assign_task/", views.assign_task, name="assign_task"),
    path("submit_task/", views.submit_task, name="submit_task"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("ratings_teams/", views.ratings_teams, name="ratings_teams"),
    path("ratings_users/", views.ratings_users, name="ratings_users"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
