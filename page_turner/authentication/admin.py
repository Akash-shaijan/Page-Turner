from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .models import Profile

class ProfileAdmin(UserAdmin):
    
    ordering = ('email',)
    
    list_display = ('email', 'is_staff', 'is_superuser')
    

    fieldsets = ( (None, {'fields': ('email', 'password')}), )
    
    add_fieldsets = ( (None, {'fields': ('email', 'password')}), )

admin.site.register(Profile, ProfileAdmin) 