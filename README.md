# A Simple Example of Django CRUD (Create, Retrieve, Update and Delete) Application Using Functional Based Views

We will use Django and functional based views to develop a simple application to allow one to create a new task, retrieve task list or a single task, update a task and delete a task. 

### Demo

If you cannot see the animated gif below, please download task_crud.gif and open it in our browser. 

![task_crud](task_crud.gif)

### Step 1: create a task app and add it to INSTALLED_APPS

First of all, use `python manage.py startapp tasks` to create a new app named "tasks" and then add it to INSTALLED_APPS in `settings.py`.

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tasks',
]
```

Then add app urls to project urls.

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls'))
]

```

### Step 2:  create Task model and associated form

Our Task model is very simple. We also used ModelForm to create a TaskForm which will then be needed to create or update a task.

```python
# tasks/models.py

from django.db import models

class Status(models.TextChoices):
    UNSTARTED = 'u', "Not started yet"
    ONGOING = 'o', "Ongoing"
    FINISHED = 'f', "Finished"


class Task(models.Model):
    name = models.CharField(verbose_name="Task name", max_length=65, unique=True)
    status = models.CharField(verbose_name="Task status", max_length=1, choices=Status.choices)

    def __str__(self):
        return self.name

# tasks/forms.py
from .models import Task
from django import forms

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = "__all__"
```

### Step 3:  Write URLConfs and associated functional based views

We will create 5 urls and 5 associated functional based views to deal with the CRUD activities. Please bear in mind that we need 2 views for the Retrieve activities: one for retrieving a list and the other for retrieving a single object.

``` tasks/urls.py
# tasks/urls.py

from django.urls import path, re_path
from . import views

# namespace
app_name = 'tasks'

urlpatterns = [

    # Create a task
    path('create/', views.task_create, name='task_create'),

    # Retrieve task list
    path('', views.task_list, name='task_list'),

    # Retrieve single task object
    re_path(r'^(?P<pk>\d+)/$', views.task_detail, name='task_detail'),

    # Update a task
    re_path(r'^(?P<pk>\d+)/update/$', views.task_update, name='task_update'),

    # Delete a task
    re_path(r'^(?P<pk>\d+)/delete/$', views.task_delete, name='task_delete'),

]
```

The code below in the core of this example. Please try to understand every line in it.

```python
# tasks/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Task
from .forms import TaskForm

# Create your views here.

# Create a task
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("tasks:task_list"))
    else:
        form = TaskForm()

    return render(request, "tasks/task_form.html", { "form": form, })


# Retrieve task list
def task_list(request):
    tasks = Task.objects.all()
    return render(request, "tasks/task_list.html", { "tasks": tasks,})


# Retrieve a single task
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, "tasks/task_detail.html", { "task": task, })


# Update a single task
def task_update(request, pk):
    task_obj = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(instance=task_obj, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("tasks:task_detail", args=[pk,]))
    else:
        form = TaskForm(instance=task_obj)

    return render(request, "tasks/task_form.html", { "form": form, "object": task_obj})


# Delete a single task
def task_delete(request, pk):
    task_obj = get_object_or_404(Task, pk=pk)
    task_obj.delete()
    return redirect(reverse("tasks:task_list"))

```

### Step 4:  Write your templates

We only need to create 3 templates: `task_list.html`, `task_detail.html` and `task_form.html`. The last template will be shared by `task_create` and `task_update` views. 

```
# tasks/templates/tasks/task_list.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Task List</title>
</head>
<body>
<h3>Task List</h3>
{% for task in tasks %}
    <p>{{ forloop.counter }}. {{ task.name }} - {{ task.get_status_display }}
        (<a href="{% url 'tasks:task_update' task.id %}">Update</a> |
        <a href="{% url 'tasks:task_delete' task.id %}">Delete</a>)
    </p>
{% endfor %}

<p> <a href="{% url 'tasks:task_create' %}"> + Add A New Task</a></p>
</body>
</html>

# tasks/templates/tasks/task_detail.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Task Detail</title>
</head>
<body>
<p> Task Name: {{ task.name }} | <a href="{% url 'tasks:task_update' task.id %}">Update</a> |
    <a href="{% url 'tasks:task_delete' task.id %}">Delete</a>
</p>
<p> Task Status: {{ task.get_status_display }} </p>
<p> <a href="{% url 'tasks:task_list' %}">View All Tasks</a> |
    <a href="{% url 'tasks:task_create'%}">New Task</a>
</p>
</body>
</html>

# tasks/templates/tasks/task_form.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% if object %}Edit Task {% else %} Create New Task {% endif %}</title>
</head>
<body>
<h3>{% if object %}Edit Task {% else %} Create New Task {% endif %}</h3>
    <form action="" method="post" enctype="multipart/form-data">
        {% csrf_token %}
        {{ form.as_p }}
        <p><input type="submit" class="btn btn-success" value="Submit"></p>
    </form>
</body>
</html>
```

### Step 5:  Run your project and test it

```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```



