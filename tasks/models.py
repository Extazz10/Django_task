from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    profile_image = models.ImageField(
        upload_to='users/profile/',
        null=True,
        blank=True,
        verbose_name='Фото профиля'
    )

    def __str__(self):
        return self.get_full_name() or self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Task(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_do_list', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return f'{self.title} ({"done" if self.completed else "todo"})'
