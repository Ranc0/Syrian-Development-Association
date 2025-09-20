from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser



@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = (
        'username', 'email', 'phone', 'user_type', 'is_verified',
        'verification_token', 'is_active'
    )
    list_filter = (
        'user_type', 'is_verified', 'is_staff', 'is_active', 'gender'
    )
    search_fields = ('username', 'email', 'phone')
    ordering = ('-created_at',)

    readonly_fields = ('created_at', 'updated_at', 'last_login')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal Info'), {
            'fields': (
                'first_name', 'last_name', 'email', 'phone', 'gender',
                'profile_picture', 'address', 'birth_date'
            )
        }),
        (_('Verification'), {
            'fields': ('verification_token', 'is_verified')
        }),
        (_('Permissions'), {
            'fields': (
                'user_type', 'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        (_('Important Dates'), {
            'fields': ('last_login', 'created_at', 'updated_at')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'phone', 'gender', 'user_type',
                'is_verified', 'verification_token',
                'password1', 'password2', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            ),
        }),
    )
@admin.register(Beneficiary)
class BeneficiaryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'residence_type', 'marital_status')
    search_fields = ('full_name', 'user__phone')

admin.site.register(MedicalAidRequest)
admin.site.register(MaterialAidRequest)
admin.site.register(ProjectRequest)
admin.site.register(Feedback)
admin.site.register(Activity)
admin.site.register(News)
admin.site.register(PendingUser)