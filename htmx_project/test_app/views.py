from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from test_app.models import Todo


def home(request):
    return render(request, 'home.html')


@login_required
def get_count_of_tasks(request):
    result = Todo.objects.by_user(request.user, with_deleted=False, with_completed=False).count()
    if result > 0:
        return HttpResponse(f"{result} tasks to do")
    else:
        return HttpResponse("Good job, you are up to date")
    

@login_required
def get_table(request):
    todos = Todo.objects.by_user(request.user, with_deleted=False, with_completed=True)
    return render(request, 'table.html', {
        "todos": todos
    })