from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'priority', 'due_date', 'completed', 'created_at')
    list_filter = ('completed', 'priority', 'due_date', 'created_at')
    search_fields = ('title', 'description', 'user__username')
    list_editable = ('completed', 'priority')
    ordering = ('completed', '-created_at')
