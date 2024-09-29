from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


# Create your models here.
class User(AbstractUser):
    patronymic = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        verbose_name="Отчество",
        help_text="Отчество пользователя",
    )
    photo = models.ImageField(
        upload_to="photos/",
        null=True,
        blank=True,
        verbose_name="Фото",
        help_text="Фотография пользователя",
    )
    xp = models.IntegerField(
        default=0,
        null=False,
        verbose_name="Опыт",
        help_text="Кол-во опыта пользователя",
    )
    level = models.IntegerField(
        default=1, null=False, verbose_name="Уровень", help_text="Уровень пользователя"
    )
    money = models.IntegerField(
        default=0,
        null=False,
        verbose_name="Монеты",
        help_text="Кол-во опыта пользователя",
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Task(models.Model):
    task_id = models.AutoField(primary_key=True, verbose_name="ID задачи")
    title = models.CharField(
        max_length=30,
        null=False,
        verbose_name="Заголовок",
        help_text="заголовок задачи",
    )
    description = models.TextField(
        null=True, blank=True, verbose_name="Описание", help_text="Описание задачи"
    )
    xp_reward = models.IntegerField(
        null=False,
        verbose_name="Награда за выполнение (XP)",
        help_text="Количество опыта за выполнение задачи",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=False,
        verbose_name="Дата создания",
        help_text="Дата создания задачи",
    )
    deadline = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Крайний срок",
        help_text="Крайний срок выполнения задачи",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ["-created_at"]


class Achievement(models.Model):
    achievement_id = models.AutoField(primary_key=True, verbose_name="ID достижения")
    photo = models.ImageField(
        upload_to="achievements/",
        null=True,
        blank=True,
        verbose_name="Фото",
        help_text="Фотография достижения",
    )
    title = models.CharField(
        max_length=30,
        null=False,
        verbose_name="Заголовок",
        help_text="Заголовок достижения",
    )
    description = models.CharField(
        max_length=100,
        null=False,
        verbose_name="Описание",
        help_text="Описание достижения",
    )
    xp_reward = models.IntegerField(
        null=False,
        verbose_name="Награда за выполнение (XP)",
        help_text="Количество опыта за получение достижения",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Достижение"
        verbose_name_plural = "Достижения"


class Team(models.Model):
    team_id = models.AutoField(primary_key=True, verbose_name="ID команды")
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        related_name="owned_teams",
        verbose_name="Владелец",
        help_text="Владелец команды",
    )
    photo = models.ImageField(
        upload_to="teams/",
        null=True,
        blank=True,
        verbose_name="Фото",
        help_text="Фотография команды",
    )
    title = models.CharField(
        max_length=30,
        null=False,
        verbose_name="Заголовок",
        help_text="Заголовок команды",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=False,
        verbose_name="Дата создания",
        help_text="Дата создания команды",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"


class TeamEmployee(models.Model):
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="members",
        verbose_name="Команда",
        help_text="Команда",
    )
    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="teams",
        verbose_name="Сотрудник",
        help_text="Сотрудник",
    )

    def __str__(self):
        return f"{self.employee.username} - {self.team.title}"

    class Meta:
        unique_together = ("team", "employee")
        verbose_name = "Член команды"
        verbose_name_plural = "Члены команды"


class AchievementEmployee(models.Model):
    achievement = models.ForeignKey(
        Achievement,
        on_delete=models.CASCADE,
        related_name="achievers",
        verbose_name="Достижение",
        help_text="Достижение",
    )
    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="achievements",
        verbose_name="Сотрудник",
        help_text="Сотрудник",
    )
    received_at = models.DateTimeField(
        auto_now_add=True,
        null=False,
        verbose_name="Дата получения",
        help_text="Дата получения достижения",
    )

    def __str__(self):
        return f"{self.employee.username} - {self.achievement.title}"

    class Meta:
        unique_together = ("achievement", "employee")
        verbose_name = "Полученное достижение"
        verbose_name_plural = "Полученные достижения"


class TaskEmployee(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="assignments",
        verbose_name="Задача",
        help_text="Задача",
    )
    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name="Сотрудник",
        help_text="Сотрудник",
    )
    took_at = models.DateTimeField(
        auto_now_add=True,
        null=False,
        verbose_name="Дата взятия задачи",
        help_text="Дата, когда задача была взята в работу",
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата завершения задачи",
        help_text="Дата, когда задача была завершена",
    )

    def __str__(self):
        return f"{self.employee.username} - {self.task.title}"

    def clean(self):
        if self.completed_at and self.took_at and self.completed_at < self.took_at:
            raise ValidationError(
                "Дата завершения не может быть раньше даты взятия задачи."
            )

    class Meta:
        unique_together = ("task", "employee")
        verbose_name = "Назначение задачи"
        verbose_name_plural = "Назначение задач"
