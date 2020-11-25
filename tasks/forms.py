#-*- coding:utf-8 -*-
from .models import Task
from django import forms

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = "__all__"
