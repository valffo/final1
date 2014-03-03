from django import forms

class TasksForm(forms.Form):
    task_title = forms.CharField()
    DATE_INPUT_FORMATS = 'd.m.Y'
    deadline_date = forms.DateField()
