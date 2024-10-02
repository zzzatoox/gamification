from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import (
    TaskEmployee,
    Achievement,
    AchievementEmployee,
    Inventory,
    TeamEmployee,
    UserProfile,
)


@receiver(post_save, sender=TaskEmployee)
def check_team_membership(sender, instance, **kwargs):
    # Достижение для состояния в 3 командах

    if TeamEmployee.objects.filter(employee=instance.employee).count() >= 3:
        achievement = Achievement.objects.filter(title="Командный Гигант").first()

        if (
            achievement
            and not AchievementEmployee.objects.filter(
                achievement=achievement, employee=instance.employee
            ).exists()
        ):
            AchievementEmployee.objects.create(
                employee=instance.employee, achievement=achievement
            )

            user_profile = instance.employee.userprofile
            user_profile.xp += achievement.xp_reward
            if achievement.coins_reward:
                user_profile.coins += achievement.coins_reward
            user_profile.update_rank()
            user_profile.save()


@receiver(post_save, sender=UserProfile)
def check_level_for_achievement(sender, instance, **kwargs):
    # Достижение для достижения уровня 10
    if instance.level >= 10:
        achievement = Achievement.objects.filter(title="Бронзовый уровень").first()
        if (
            achievement
            and not AchievementEmployee.objects.filter(
                achievement=achievement, employee=instance.user
            ).exists()
        ):
            AchievementEmployee.objects.create(
                employee=instance.user, achievement=achievement
            )

            instance.xp += achievement.xp_reward
            if achievement.coins_reward:
                instance.coins += achievement.coins_reward
            instance.update_rank()
            instance.save()

        elif instance.level == 50:
            achievement = Achievement.objects.filter(title="Серебряный уровень").first()
            if (
                achievement
                and not AchievementEmployee.objects.filter(
                    achievement=achievement, employee=instance.user
                ).exists()
            ):
                AchievementEmployee.objects.create(
                    employee=instance.user, achievement=achievement
                )

                instance.xp += achievement.xp_reward
                if achievement.coins_reward:
                    instance.coins += achievement.coins_reward
                instance.update_rank()
                instance.save()
        elif instance.level == 80:
            achievement = Achievement.objects.filter(title="Золотой уровень").first()
            if (
                achievement
                and not AchievementEmployee.objects.filter(
                    achievement=achievement, employee=instance.user
                ).exists()
            ):
                AchievementEmployee.objects.create(
                    employee=instance.user, achievement=achievement
                )

                instance.xp += achievement.xp_reward
                if achievement.coins_reward:
                    instance.coins += achievement.coins_reward
                instance.update_rank()
                instance.save()


@receiver(post_save, sender=TaskEmployee)
def check_task_completion(sender, instance, **kwargs):
    # Выполнение задания
    if instance.status.title == "Выполнено" and instance.completed_at:
        # Проверяем, есть ли достижения для выполнения одной задачи
        achievement = Achievement.objects.filter(title="Начало").first()
        if (
            achievement
            and not AchievementEmployee.objects.filter(
                achievement=achievement, employee=instance.employee
            ).exists()
        ):
            AchievementEmployee.objects.create(
                achievement=achievement, employee=instance.employee
            )

            user_profile = instance.employee.userprofile
            user_profile.xp += achievement.xp_reward
            if achievement.coins_reward:
                user_profile.coins += achievement.coins_reward
            user_profile.update_rank()
            user_profile.save()

        # Проверяем, есть ли достижения для убийства гоблинов

        completed_goblin_tasks = TaskEmployee.objects.filter(
            employee=instance.employee,
            status__title="Выполнено",
        ).count()
        if completed_goblin_tasks == 10:
            achievement = Achievement.objects.filter(
                title="Бронзовый убийца гоблинов"
            ).first()
            if (
                achievement
                and not AchievementEmployee.objects.filter(
                    achievement=achievement, employee=instance.employee
                ).exists()
            ):
                AchievementEmployee.objects.create(
                    achievement=achievement, employee=instance.employee
                )
                user_profile = instance.employee.userprofile
                user_profile.xp += achievement.xp_reward
                if achievement.coins_reward:
                    user_profile.coins += achievement.coins_reward
                user_profile.update_rank()
                user_profile.save()
        elif completed_goblin_tasks == 50:
            achievement = Achievement.objects.filter(
                title="Серебряный убийца гоблинов"
            ).first()
            if (
                achievement
                and not AchievementEmployee.objects.filter(
                    achievement=achievement, employee=instance.employee
                ).exists()
            ):
                AchievementEmployee.objects.create(
                    achievement=achievement, employee=instance.employee
                )
                user_profile = instance.employee.userprofile
                user_profile.xp += achievement.xp_reward
                if achievement.coins_reward:
                    user_profile.coins += achievement.coins_reward
                user_profile.update_rank()
                user_profile.save()
        elif completed_goblin_tasks == 100:
            achievement = Achievement.objects.filter(
                title="Золотой убийца гоблинов"
            ).first()
            if (
                achievement
                and not AchievementEmployee.objects.filter(
                    achievement=achievement, employee=instance.employee
                ).exists()
            ):
                AchievementEmployee.objects.create(
                    achievement=achievement, employee=instance.employee
                )
                user_profile = instance.employee.userprofile
                user_profile.xp += achievement.xp_reward
                if achievement.coins_reward:
                    user_profile.coins += achievement.coins_reward
                user_profile.update_rank()
                user_profile.save()


@receiver(post_save, sender=Inventory)
def check_inventory_changes(sender, instance, **kwargs):
    # Изменение инвентаря
    achievement = Achievement.objects.filter(title="Мастер Артефактов").first()
    if (
        achievement
        and not AchievementEmployee.objects.filter(
            achievement=achievement, employee=instance.user
        ).exists()
    ):
        AchievementEmployee.objects.create(
            achievement=achievement, employee=instance.user
        )
        user_profile = instance.user.userprofile
        user_profile.xp += achievement.xp_reward
        if achievement.coins_reward:
            user_profile.coins += achievement.coins_reward
        user_profile.update_rank()
        user_profile.save()
