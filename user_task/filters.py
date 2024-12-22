from django_filters import rest_framework as filters
from django.db.models import Q


class UserTaskBookmarkFilter(filters.DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        queryset = super().filter_queryset(request, queryset, view)
        if view.action == "list":
            search_query = request.query_params.get("search")
            print(search_query)
            if search_query:
                queryset = queryset.filter(
                    Q(name__icontains=search_query) |
                    Q(description__icontains=search_query),

                )
        return queryset


