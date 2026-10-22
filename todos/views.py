from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Task
from .forms import TaskForm, UserRegisterForm


@login_required
def task_list_view(request):
    """Display the list of tasks belonging to the logged-in user with filtering and search."""
    user_tasks = Task.objects.filter(user=request.user)

    # Search filter
    search_query = request.GET.get('q', '').strip()
    if search_query:
        user_tasks = user_tasks.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )

    # Status filter
    status_filter = request.GET.get('status', 'all')
    if status_filter == 'active':
        user_tasks = user_tasks.filter(completed=False)
    elif status_filter == 'completed':
        user_tasks = user_tasks.filter(completed=True)

    # Priority filter
    priority_filter = request.GET.get('priority', 'all')
    if priority_filter in ['LOW', 'MEDIUM', 'HIGH']:
        user_tasks = user_tasks.filter(priority=priority_filter)

    # Metrics for progress dashboard
    all_tasks = Task.objects.filter(user=request.user)
    total_count = all_tasks.count()
    completed_count = all_tasks.filter(completed=True).count()
    pending_count = total_count - completed_count
    completion_rate = int((completed_count / total_count * 100)) if total_count > 0 else 0

    context = {
        'tasks': user_tasks,
        'search_query': search_query,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'total_count': total_count,
        'completed_count': completed_count,
        'pending_count': pending_count,
        'completion_rate': completion_rate,
    }
    return render(request, 'todos/task_list.html', context)


@login_required
def task_create_view(request):
    """Create a new task for the current authenticated user."""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, f'Task "{task.title}" created successfully!')
            return redirect('task_list')
    else:
        form = TaskForm()

    return render(request, 'todos/task_form.html', {
        'form': form,
        'page_title': 'Add New Task',
        'is_edit': False,
    })


@login_required
def task_update_view(request, pk):
    """Edit an existing task owned by the current authenticated user."""
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f'Task "{task.title}" updated successfully!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'todos/task_form.html', {
        'form': form,
        'task': task,
        'page_title': 'Edit Task',
        'is_edit': True,
    })


@login_required
def task_delete_view(request, pk):
    """Delete a task after user confirmation."""
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == 'POST':
        title = task.title
        task.delete()
        messages.success(request, f'Task "{title}" was deleted.')
        return redirect('task_list')

    return render(request, 'todos/task_confirm_delete.html', {'task': task})


@login_required
def task_toggle_complete_view(request, pk):
    """Toggle a task between completed and incomplete status."""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.completed = not task.completed
    task.save()

    if task.completed:
        messages.success(request, f'✓ Marked "{task.title}" as completed!')
    else:
        messages.info(request, f'Marked "{task.title}" as active.')

    return redirect('task_list')


def register_view(request):
    """User registration view with auto-login upon successful registration."""
    if request.user.is_authenticated:
        return redirect('task_list')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Your account has been registered.')
            return redirect('task_list')
    else:
        form = UserRegisterForm()

    return render(request, 'todos/register.html', {'form': form})


def login_view(request):
    """User login view."""
    if request.user.is_authenticated:
        return redirect('task_list')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next') or 'task_list'
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = AuthenticationForm()

    return render(request, 'todos/login.html', {'form': form})


def logout_view(request):
    """User logout view."""
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, 'You have been logged out.')
    return redirect('login')
