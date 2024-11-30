from .models import TaskCategory, Task
from django.db.models import Q


def get_tasks_by_task_category(category_id, queryset):
    queryset = queryset.filter(category__id=category_id)
    return queryset


def search_in_task_and_task_category(search):
    qs = TaskCategory.objects.filter(
        title__icontains=search
    )
    if qs.exists():
        return qs
    
    qs = Task.objects.filter(
        Q(name__icontains=search)
    )
    qs = TaskCategory.objects.filter(
        categories_tasks__in=qs.values_list("id", flat=True)
    )
    return qs

