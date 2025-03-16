from django.contrib import admin

#role
from .models import User, PasswordReset
#import models

admin.site.register(PasswordReset)

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'role')}),
        ('Permissions', {'fields': ('is_staff', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)
    

    # list_display = ('username', 'email', 'is_company', 'is_investor', 'is_admin')
    # list_filter = ('is_company', 'is_investor', 'is_admin')
    # fieldsets = (
    #     (None, {'fields': ('username', 'password')}),
    #     ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'is_company', 'is_investor')}),
    #     ('Permissions', {'fields': ('is_admin', 'groups', 'user_permissions')}),
    #     ('Important dates', {'fields': ('last_login', 'date_joined')}),
    # )
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('username', 'email', 'password1', 'password2', 'is_company', 'is_investor'),
    #     }),
    # )
    # search_fields = ('username', 'email')
    # ordering = ('username',)