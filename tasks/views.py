from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .models import Task
from .forms import TaskForm, RegistrationForm, LoginForm

class UserLoginView(auth_views.LoginView):
    template_name = 'tasks/login.html'
    authentication_form = LoginForm

def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('tasks:login')

def registration_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно. Добро пожаловать!')
            return redirect('tasks:index')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = RegistrationForm()
    return render(request, 'tasks/registration.html', {'form': form})

@login_required
def index(request):
    q = request.GET.get('q', '').strip()
    tasks_qs = Task.objects.filter(owner=request.user)
    if q:
        tasks_qs = tasks_qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
    paginator = Paginator(tasks_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'tasks/index.html', {'tasks': page_obj, 'q': q})

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            messages.success(request, 'Задача успешно создана.')
            return redirect('tasks:index')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Задача обновлена.')
            return redirect('tasks:index')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'task': task})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Задача удалена.')
        return redirect('tasks:index')
    return render(request, 'tasks/confirm_delete.html', {'task': task})

@login_required
def toggle_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    task.completed = not task.completed
    task.save()
    messages.info(request, f'Задача "{task.title}" помечена как '
                           f'{"выполненная" if task.completed else "невыполненная"}.')
    return redirect('tasks:index')

