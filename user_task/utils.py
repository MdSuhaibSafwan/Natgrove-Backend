from .models import TaskCategory, Task
from django.db.models import Q


def get_tasks_by_filtering(category_id, search, queryset):
    if category_id:
        queryset = queryset.filter(category__id=category_id)
        
    if search:
        queryset = queryset.filter(Q(name=search) | Q(description=search))

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

