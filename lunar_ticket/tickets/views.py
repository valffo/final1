# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from datetime import date

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from models import Task
from forms import TasksForm
from django.views import generic
from django.core.urlresolvers import reverse


# Create your views here.

STATUSES = {
    'today': u'Задачи на сегодня',
    'someday': u'Все задачи' ,
    'fixed': u'Выпоненые задачи'
    }
ACTION_DELETE = {'delete': u"Удалить выбраные", }
ACTION_SET_FIXED = {'set_fixed': u'Отметить выбраные как выполненные', }
ACTION_SET_NOT_FIXED = {'set_not_fixed': u'Отметить выбраные как не выполненные', }

@login_required
def index(request, status, message=''):
    actions = {}
    if status == 'today':
        latest_tasks_list = Task.objects.filter(deadline_date=date.today(), user=request.user.id).order_by('-deadline_date')[:5]
        actions.update(ACTION_DELETE)
        actions.update(ACTION_SET_FIXED)
        actions.update(ACTION_SET_NOT_FIXED)
    elif status == 'fixed':
        latest_tasks_list = Task.objects.filter(done=1, user=request.user.id).order_by('-deadline_date')[:5]
        actions = ACTION_DELETE
    else:
        latest_tasks_list = Task.objects.filter(user=request.user.id).order_by('-deadline_date')[:5]
        actions.update(ACTION_DELETE)
        actions.update(ACTION_SET_FIXED)
        actions.update(ACTION_SET_NOT_FIXED)
    template = loader.get_template('tickets/index.html')
    context = RequestContext(request, {
        'latest_tasks_list': latest_tasks_list,
        'status': status,
        'actions': actions,
        'statuses': STATUSES,
        'userg': str(request.user.id) + '   ' + request.user.username,
        'message': message
    })
    return HttpResponse(template.render(context))

@login_required
def add(request):
    if request.method == 'POST':
        form = TasksForm(request.POST)
        if form.is_valid():
            task = Task(
                deadline_date=request.POST['deadline_date'],
                task_title=request.POST['task_title'],
                user_id=request.user.id,
            )
            task.save()
            return HttpResponseRedirect(reverse('detail', kwargs={'pk': task.id, }))
    else:
        form = TasksForm()

    return render(request, 'tickets/add.html', {'form': form, })

def do_action(request):
    task_id = request.POST.getlist('task_id[]')
    action = request.POST['act']
    status = request.POST['status']
    if (ACTION_DELETE.has_key(action)):
        tasks = Task.objects.filter(id__in=task_id, ).delete()
    elif (ACTION_SET_FIXED.has_key(action)):
        tasks = Task.objects.filter(id__in=task_id).update(done=True)
    elif (ACTION_SET_NOT_FIXED.has_key(action)):
        tasks = Task.objects.filter(id__in=task_id).update(done=False)
    return HttpResponseRedirect(reverse('tasks_index', kwargs={'status': status, }))

class DetailView(generic.DetailView):
    model = Task
    template_name = 'tickets/detail.html'
