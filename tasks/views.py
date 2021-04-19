from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from .models import Task
from .forms import TaskForm

# Create your views here.
# Functional based view
# Create a task
# def task_create(request):
#     if request.method == "POST":
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect(reverse("tasks:task_list"))
#     else:
#         form = TaskForm()
#
#     return render(request, "tasks/task_form.html", { "form": form, })
#
#
# # Retrieve task list
# def task_list(request):
#     tasks = Task.objects.all()
#     return render(request, "tasks/task_list.html", { "tasks": tasks,})
#
#
# # Retrieve a single task
# def task_detail(request, pk):
#     task = get_object_or_404(Task, pk=pk)
#     return render(request, "tasks/task_detail.html", { "task": task, })
#
#
# # Update a single task
# def task_update(request, pk):
#     task_obj = get_object_or_404(Task, pk=pk)
#     if request.method == 'POST':
#         form = TaskForm(instance=task_obj, data=request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect(reverse("tasks:task_detail", args=[pk,]))
#     else:
#         form = TaskForm(instance=task_obj)
#
#     return render(request, "tasks/task_form.html", { "form": form, "object": task_obj})
#
#
# # Delete a single task
# def task_delete(request, pk):
#     task_obj = get_object_or_404(Task, pk=pk)
#     task_obj.delete()
#     return redirect(reverse("tasks:task_list"))

# Class Based Views
from django.views.generic import ListView, DetailView, \
    CreateView, UpdateView, DeleteView

class TaskListView(ListView):
    model = Task
    context_object_name = 'tasks'

class TaskDetailView(DetailView):
    model = Task

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks:task_list')

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks:task_list')

class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('tasks:task_list')
