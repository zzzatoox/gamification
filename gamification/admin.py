from django.contrib import admin
from .models import (
    User,
    Task,
    Achievement,
    Team,
    TeamEmployee,
    AchievementEmployee,
    TaskEmployee,
    Product,
    Inventory,
    Notification,
    Rank,
    UserProfile,
    Status,
)


# Register your models here.
admin.site.register(User)
admin.site.register(Task)
admin.site.register(Achievement)
admin.site.register(Team)
admin.site.register(TeamEmployee)
admin.site.register(AchievementEmployee)
admin.site.register(TaskEmployee)
admin.site.register(Product)
admin.site.register(Inventory)
admin.site.register(Notification)
admin.site.register(Rank)
admin.site.register(UserProfile)
admin.site.register(Status)
