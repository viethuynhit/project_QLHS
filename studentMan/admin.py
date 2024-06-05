from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'role', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('username', 'role', 'is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('role','is_active', 'is_staff', 'is_superuser',
            'name', 'dateOfBirth', 'sex', 'phone', 'email', 'address')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role', 'is_active', 'is_staff', 
                'is_superuser','name', 'dateOfBirth', 'sex', 'phone', 'email', 'address')}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)


admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Age)
admin.site.register(ClassOfSchool)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Admin)
admin.site.register(Mark)