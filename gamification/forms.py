from django import forms
from .models import Task


class CreateTaskForm(forms.ModelForm):
    model = Task
    fields = ["title", "description", "xp_reward", "deadline"]
    labels = {
        "title": "Заголовок",
        "description": "Описание",
        "xp_reward": "Награда за выполнение (XP)",
        "deadline": "Крайний срок",
    }
    help_text = {
        "title": "Заголовок задачи",
        "description": "Описание задачи",
        "xp_reward": "Кол-во опыта за выполнение задачи",
        "deadline": "Крайний срок выполнения задачи",
    }
