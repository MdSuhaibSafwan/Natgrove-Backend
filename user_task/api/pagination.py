from rest_framework.pagination import BasePagination
from django.utils.translation import gettext_lazy as _


class TaskCategoryPagination(BasePagination):
    page_size = 10    
    page_query_param = 'page'
    invalid_page_message = _('Invalid page.')


class TaskPagination(BasePagination):
    page_size = 10    
    page_query_param = 'page'
    invalid_page_message = _('Invalid page.')

