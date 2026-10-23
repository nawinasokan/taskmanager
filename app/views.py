from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import TaskForm
from .models import Task


def task_list(request):
    tasks = Task.objects.order_by('-created_at')

    status = request.GET.get('status', 'all')
    if status == 'pending':
        tasks = tasks.filter(completed=False)
    elif status == 'completed':
        tasks = tasks.filter(completed=True)

    query = request.GET.get('q', '').strip()
    if query:
        tasks = tasks.filter(Q(title__icontains=query) | Q(description__icontains=query))

    context = {'tasks': tasks, 'status': status, 'query': query}
    return render(request, 'app/task_list.html', context)


def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task created.')
            return redirect('app:task_list')
    else:
        form = TaskForm()
    return render(request, 'app/task_form.html', {'form': form, 'heading': 'New Task'})


def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated.')
            return redirect('app:task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'app/task_form.html', {'form': form, 'heading': 'Edit Task'})


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted.')
        return redirect('app:task_list')
    return render(request, 'app/task_confirm_delete.html', {'task': task})


@require_POST
def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.completed = not task.completed
    task.save()
    messages.info(request, 'Marked as done.' if task.completed else 'Marked as pending.')
    return redirect('app:task_list')
