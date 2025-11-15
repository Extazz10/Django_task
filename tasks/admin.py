from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Task

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Profile', {'fields': ('profile_image',)}),
    )

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'completed', 'created_at')
    list_filter = ('completed', 'created_at')
    search_fields = ('title', 'description', 'owner__username')
