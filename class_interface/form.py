# -*-coding: utf-8 -*-
from django import forms


class HomeworkForm(forms.Form):
    name = forms.CharField(max_length=300)
    homework_img = forms.ImageField()
