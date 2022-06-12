from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'is_staff', 'is_superuser', 'is_active', 'created_date', 'updated_date']
    list_filter = ['is_staff', 'is_superuser', 'is_active']
    ordering = ['-created_date']
    fieldsets = (
        ('Authentication', {
            'fields': (
                'email', 'password'
                )
        }),
        ('Permissions', {
            'fields': (
                'is_staff', 'is_active', 'is_superuser'
                )
        }),
    )
    add_fieldsets = (
        ('User info', {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser')}
        ),
    )
admin.site.register(User, CustomUserAdmin)