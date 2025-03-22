from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from test_app.models import Todo


def home(request):
    return render(request, 'home.html')


@login_required
def get_count_of_tasks(request):
    result = Todo.objects.by_user(request.user, active_only=False).count()
    if result > 0:
        return HttpResponse(f"{result} tasks to do")
    else:
        return HttpResponse("Good job, you are up to date")