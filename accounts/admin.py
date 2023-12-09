from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserAccount

class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'email', 'phone_number', 'is_active', 'role', 'subscription_plan','is_superuser')
    search_fields = ('email', 'phone_number')
    
    # Specify a valid field for ordering, for example, 'id'
    ordering = ('id',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name' ,'role', 'subscription_plan','phone_number', 'display_pic')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Qualifications',{'fields': ('city','state','country','qualification','skills','subjects','category')})
        # ('Important dates', {'fields': ('last_login',)}),
    )

admin.site.register(UserAccount, CustomUserAdmin)
