from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    task_title = models.CharField(max_length=200)
    deadline_date = models.DateField()
    done = models.BooleanField(default=False)
    user = models.ForeignKey(User)
