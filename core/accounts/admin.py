from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User, Profile

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'is_staff', 'is_superuser', 'is_active', 'is_verified', 'created_date', 'updated_date']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'is_verified']
    ordering = ['-created_date']
    fieldsets = (
        ('Authentication', {
            'fields': (
                'email', 'password'
                )
        }),
        ('Permissions', {
            'fields': (
                'is_staff', 'is_active', 'is_superuser', 'is_verified'
                )
        }),
        ('Group permissions', {
            'fields': (
                'groups', 'user_permissions'
                )
        }),
        ('Important date', {
            'fields': (
                'last_login',
                )
        }),
    )
    add_fieldsets = (
        ('User info', {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_verified', 'is_superuser')}
        ),
    )
admin.site.register(User, CustomUserAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'image', 'description', 'created_date', 'updated_date']
    search_fields = ['user', 'first_name', 'last_name']    
    ordering = ['-created_date']
admin.site.register(Profile, ProfileAdmin)

