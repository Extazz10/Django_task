from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Task

User = get_user_model()

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4})
        }

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'profile_image')

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={'placeholder': 'Введите логин', 'class': 'form-control'})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль', 'class': 'form-control'})
    )