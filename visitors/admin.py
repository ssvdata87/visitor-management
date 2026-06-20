from django.contrib import admin
from django.utils import timezone
from .models import Visitor, Host, Visit


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'email', 'company_name', 'created_at')
    search_fields = ('full_name', 'phone_number', 'email', 'company_name')
    list_filter = ('id_proof_type', 'created_at')
    ordering = ('full_name',)


@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'designation', 'phone_number', 'is_active')
    search_fields = ('name', 'department', 'email')
    list_filter = ('department', 'is_active')


@admin.action(description="Check out selected visits now")
def check_out_now(modeladmin, request, queryset):
    queryset.filter(status='CHECKED_IN').update(
        status='CHECKED_OUT', check_out_time=timezone.now()
    )


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = (
        'visitor', 'host', 'purpose', 'status',
        'check_in_time', 'check_out_time', 'badge_number',
    )
    list_filter = ('status', 'purpose', 'host', 'check_in_time')
    search_fields = (
        'visitor__full_name', 'visitor__phone_number',
        'host__name', 'badge_number',
    )
    autocomplete_fields = ('visitor', 'host')
    date_hierarchy = 'check_in_time'
    actions = [check_out_now]
