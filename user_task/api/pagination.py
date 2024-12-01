from rest_framework.pagination import BasePagination, PageNumberPagination
from django.utils.translation import gettext_lazy as _


class TaskCategoryPagination(PageNumberPagination):
    page_size = 10    
    page_query_param = 'page'
    invalid_page_message = _('Invalid page.')


class TaskPagination(PageNumberPagination):
    page_size = 10    
    page_query_param = 'page'
    invalid_page_message = _('Invalid page.')

