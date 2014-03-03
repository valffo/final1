from django.contrib import admin
from models import Task
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin

admin.site.unregister(User)

class TaskInline(admin.TabularInline):
    pass
# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    # ...
    list_display = ('task_title', 'user', 'deadline_date', 'done',)
    list_filter = ['user', 'done']
    search_fields = ['task_title']
admin.site.register(Task, TaskAdmin)

class RegUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_superuser', 'is_active',)

admin.site.register(User, RegUserAdmin)
