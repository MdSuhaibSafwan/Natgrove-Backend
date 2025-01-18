from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import Company, UserProfile

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ['email', 'is_admin']
    list_filter = ['is_admin']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ("first_name", "middle_name", "last_name", "phone_number")}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password_2')}
        ),
    )

    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
admin.site.register(Company)
