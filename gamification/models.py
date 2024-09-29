from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# Create your models here.
class User(AbstractUser):
    patronymic = models.CharField(max_length=150, null=True, blank=True)
    photo = models.ImageField(upload_to="photos/", null=True, blank=True)
    xp = models.IntegerField(default=0, null=False)
    level = models.IntegerField(default=1, null=False)
    money = models.IntegerField(default=0, null=False)

    def __str__(self):
        return self.username


class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30, null=False)
    description = models.TextField()
    xp_reward = models.IntegerField(null=False)
    created_at = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return self.title


class Achievement(models.Model):
    achievement_id = models.AutoField(primary_key=True)
    photo = models.ImageField(upload_to="achievements/", null=True, blank=True)
    title = models.CharField(max_length=30, null=False)
    description = models.CharField(max_length=100, null=False)
    xp_reward = models.IntegerField(null=False)

    def __str__(self):
        return self.title


class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    photo = models.ImageField(upload_to="teams/", null=True, blank=True)
    title = models.CharField(max_length=30, null=False)
    created_at = models.DateTimeField(default=timezone.now, null=False)
    # Поле xp рассчитывается в зависимости от общего среднего xp всех участников,
    # и изменяется оно только тогда, когда кто-то из команды получает опыт
    xp = models.IntegerField(default=0, null=False)
    def __str__(self):
        return self.title


class TeamEmployee(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("team", "employee")


class AchievementEmployee(models.Model):
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    received_at = models.DateTimeField(default=timezone.now, null=False)

    class Meta:
        unique_together = ("achievement", "employee")


class TaskEmployee(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    took_at = models.DateTimeField(null=False)
    completed_at = models.DateTimeField(null=False)

    class Meta:
        unique_together = ("task", "employee")
