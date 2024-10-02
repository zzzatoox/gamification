from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


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

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        first_rank = Rank.objects.order_by("level").first()
        user_profile = UserProfile.objects.create(user=instance, rank=first_rank)

        # выдаю достижение "Меч в сердце"
        achievement = Achievement.objects.filter(title="Меч в сердце").first()
        if (
            achievement
            and not AchievementEmployee.objects.filter(
                achievement=achievement, employee=instance
            ).exists()
        ):
            AchievementEmployee.objects.create(
                achievement=achievement, employee=instance
            )

            user_profile.xp += achievement.xp_reward
            if achievement.coins_reward:
                user_profile.coins += achievement.coins_reward
            user_profile.update_rank()
            user_profile.save()


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
    xp = models.PositiveIntegerField(
        null=False,
        default=0,
        verbose_name="Опыт",
        help_text="Опыт команды",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"

    def update_xp(self):
        total_xp = sum(member.employee.userprofile.xp for member in self.members.all())
        self.xp = total_xp
        self.save()


class Status(models.Model):
    status_id = models.AutoField(primary_key=True, verbose_name="ID статуса")
    title = models.CharField(
        max_length=30,
        null=False,
        verbose_name="Заголовок",
        help_text="Заголовок статуса",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"


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
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Команда",
        help_text="Команда, к которой относится задача",
    )
    xp_reward = models.PositiveIntegerField(
        null=False,
        verbose_name="Награда за выполнение (XP)",
        help_text="Количество опыта за выполнение задачи",
    )
    coins_reward = models.PositiveIntegerField(
        null=False,
        verbose_name="Награда за выполнение (монеты)",
        help_text="Количество монет за выполнение задачи",
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
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        null=False,
        default=1,
        verbose_name="Статус",
        help_text="Статус выполнения задачи",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ["-created_at"]


class Achievement(models.Model):
    achievement_id = models.AutoField(
        primary_key=True,
        verbose_name="ID достижения",
    )
    photo = models.ImageField(
        upload_to="achievements/",
        null=False,
        verbose_name="Фото",
        help_text="Фотография достижения",
    )
    title = models.CharField(
        max_length=30,
        null=False,
        verbose_name="Заголовок",
        help_text="Заголовок достижения",
    )
    description = models.TextField(
        null=False,
        verbose_name="Описание",
        help_text="Описание достижения",
    )
    xp_reward = models.PositiveIntegerField(
        null=False,
        verbose_name="Награда за выполнение (XP)",
        help_text="Количество опыта за получение достижения",
    )
    coins_reward = models.PositiveIntegerField(
        null=True,
        verbose_name="Награда за выполнение (монеты)",
        help_text="Количество монет за получение достижения",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Достижение"
        verbose_name_plural = "Достижения"


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


@receiver(post_save, sender=TeamEmployee)
def update_team_xp_on_join(sender, instance, **kwargs):
    instance.team.update_xp()


@receiver(post_delete, sender=TeamEmployee)
def update_team_xp_on_leave(sender, instance, **kwargs):
    instance.team.update_xp()


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


# @receiver(post_save, sender=AchievementEmployee)
# def update_user_profile_on_achievement(sender, instance, **kwargs):
#     user_profile = instance.employee.userprofile
#     achievement = instance.achievement
#     user_profile.xp += achievement.xp_reward
#     if achievement.coins_reward:
#         user_profile.coins += achievement.coins_reward
#     user_profile.update_rank()
#     user_profile.save()


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
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        null=True,
        default=1,
        verbose_name="Статус",
        help_text="Статус выполнения задачи",
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


class Product(models.Model):
    product_id = models.AutoField(primary_key=True, verbose_name="ID товара")
    title = models.CharField(
        max_length=50,
        null=False,
        verbose_name="Название",
        help_text="Название товара",
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Описание",
        help_text="Описание товара",
    )
    price = models.PositiveIntegerField(
        default=0,
        null=False,
        verbose_name="Цена",
        help_text="Цена товара",
    )
    photo = models.ImageField(
        upload_to="products/",
        null=True,
        blank=True,
        verbose_name="Фото",
        help_text="Фотография товара",
    )
    is_available = models.BooleanField(
        default=True,
        null=False,
        verbose_name="Доступен",
        help_text="Флаг, показывающий, доступен ли товар",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["-price"]


class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True, verbose_name="ID инвентаря")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        return f"{self.user.username} - {self.product.title} ({self.quantity})"

    class Meta:
        verbose_name = "Инвентарь"
        verbose_name_plural = "Инвентари"
        ordering = ["-date_added"]


class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True, verbose_name="ID уведомления")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    message = models.TextField(verbose_name="Сообщение")
    is_read = models.BooleanField(default=False, verbose_name="Прочитано")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.user.username} - {self.message[:50]}"

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
        ordering = ["-created_at"]


class Rank(models.Model):
    rank_id = models.AutoField(primary_key=True, verbose_name="ID звания")
    title = models.CharField(max_length=50, verbose_name="Звание")
    level = models.PositiveIntegerField(verbose_name="Уровень")
    required_xp = models.PositiveIntegerField(verbose_name="Требуемый опыт")
    bonus_coins = models.PositiveIntegerField(verbose_name="Надбавка (монеты)")

    def __str__(self):
        return f"{self.title} (Уровень {self.level})"

    class Meta:
        verbose_name = "Звание"
        verbose_name_plural = "Звания"
        ordering = ["level"]


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    xp = models.PositiveIntegerField(
        default=0,
        null=False,
        verbose_name="Опыт",
        help_text="Кол-во опыта пользователя",
    )
    level = models.PositiveIntegerField(
        default=1,
        null=False,
        verbose_name="Уровень",
        help_text="Уровень пользователя",
    )
    coins = models.PositiveIntegerField(
        default=0,
        null=False,
        verbose_name="Монеты",
        help_text="Монеты пользователя",
    )
    rank = models.ForeignKey(
        Rank,
        default=1,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Звание",
        help_text="Звание пользователя",
    )

    def __str__(self):
        return f"{self.user.username} (Уровень {self.level})"

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def update_rank(self):
        # Получаем все звания, отсортированные по уровню
        ranks = Rank.objects.order_by("level")
        for rank in ranks:
            if self.xp >= rank.required_xp:
                self.rank = rank
                self.level = rank.level
        self.save()

    def complete_task(self, task_xp, task_coins):
        # Добавляем опыт и монеты за задание
        self.xp += task_xp
        self.coins += task_coins

        # Добавляем надбавку за звание
        if self.rank:
            self.coins += self.rank.bonus_coins

        # Обновляем ранг и уровень
        self.update_rank()
        self.save()
