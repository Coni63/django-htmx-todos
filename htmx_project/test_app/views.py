from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
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

@login_required
def toggle_todo(request, todo_id):
    """Toggles the completion status of a task."""
    if request.method == "POST":
        todo = get_object_or_404(Todo, id=todo_id, created_by=request.user)
        todo.toggle_complete()
        todo.save()

        # Re-render the updated row
        response = render(request, 'table_row.html', {'todo': todo})
        response['HX-Trigger'] = 'refresh-counter'
        return response

    return HttpResponseNotAllowed(["POST"])


@login_required
def delete_todo(request, todo_id):
    """Deletes a task via HTMX."""
    if request.method == "DELETE":
        todo = get_object_or_404(Todo, id=todo_id, created_by=request.user)
        todo.soft_delete()

        response = HttpResponse("")  # HTMX will remove the row
        response['HX-Trigger'] = 'refresh-counter'
        return response

    return HttpResponseNotAllowed(["DELETE"])


@login_required
def add_todo(request):
    """Adds a new todo item."""
    if request.method == "POST":
        title = request.POST.get('title', '').strip()
        if title:
            # Create new todo with the current user
            todo = Todo.objects.create(
                title=title,
                created_by=request.user
            )
            
            # Render just the new row and trigger counter refresh
            response = render(request, 'table_row.html', {'todo': todo})
            response['HX-Trigger'] = 'refresh-counter'
            return response
            
    return HttpResponseBadRequest("Invalid request")