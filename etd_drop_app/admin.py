from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext, ugettext_lazy as _

# Don't use the default admin interfaces
admin.site.unregister(Group)
admin.site.unregister(User)

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        #(_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': (
            #'is_active', 
            'is_staff', 
            'is_superuser',
        )}),
        (_('Important dates'), {'fields': (
            'last_login', 
            'date_joined',
        )}),
    )
    readonly_fields = ('username', 'date_joined', 'last_login')
    list_display = (
        'username', 
        #'email', 
        #'is_active', 
        'is_staff', 
        'is_superuser', 
        'date_joined', 
        'last_login',
    )
admin.site.register(User, CustomUserAdmin)
