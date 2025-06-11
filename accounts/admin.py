# # core/admin.py or accounts/admin.py
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .models import User


# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     # Customize as needed
#     list_display = ('username', 'email', 'is_staff', 'is_active')
#     search_fields = ('username', 'email')
#     list_filter = ('is_staff', 'is_active')
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email')
    ordering = ('date_joined',)
    readonly_fields = ('date_joined',)
