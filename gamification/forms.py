from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Task, Team, User


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("title", "description", "team", "xp_reward", "coins_reward")


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ("title", "photo")


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=255, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "full_name", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if "@" in username:
            raise forms.ValidationError("Логин не может содержать символ '@'")
        return username

    def clean_full_name(self):
        full_name = self.cleaned_data.get("full_name")
        names = full_name.strip().split()
        if len(names) < 2:
            raise forms.ValidationError(
                "Введите ФИО корректно, каждое слово через пробел"
            )
        return full_name

    def save(self, commit=True):
        user = super().save(commit=False)
        full_name = self.cleaned_data["full_name"].split()
        user.last_name = full_name[0]
        user.first_name = full_name[1]
        user.patronymic = full_name[-1] if len(full_name) > 2 else ""
        if commit:
            user.save()
        return user
