from django.contrib import admin
from test_app.models import Todo


class TodoAdmin(admin.ModelAdmin):
    pass


admin.site.register(Todo, TodoAdmin)