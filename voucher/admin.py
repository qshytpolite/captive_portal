import csv
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect
from django.utils.http import urlencode
from django.http import HttpResponse
from django.contrib import admin
from .models import Voucher, VoucherUsage, VoucherGenerationLog
from .forms import VoucherForm, VoucherAdminForm
from .services import create_vouchers
from django.db import models


@admin.action(description="Export selected vouchers as CSV")
def export_vouchers_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="vouchers.csv"'

    writer = csv.writer(response)
    writer.writerow(['Code', 'Business', 'Duration (mins)',
                    'Expires At', 'Is Active', 'Created By', 'Created At'])

    for voucher in queryset:
        writer.writerow([
            voucher.code,
            voucher.business.name,
            voucher.duration_minutes,
            voucher.expires_at,
            voucher.is_active,
            voucher.created_by.username if voucher.created_by else '',
            voucher.created_at.strftime('%Y-%m-%d %H:%M')
        ])

    return response

# link to view generated vouchers in django admin


def create_vouchers_and_redirect(modeladmin, request, queryset):
    business = queryset.first()  # Or from form input
    created = create_vouchers(business, count=10, created_by=request.user)

    codes = [v.code for v in created]
    filter_param = urlencode({'code__in': ','.join(codes)})

    link = reverse("admin:voucher_voucher_changelist") + f"?{filter_param}"
    messages.success(request, f"{len(codes)} vouchers created. "
                     f"<a href='{link}'>View them here</a>.", extra_tags="safe")

    return redirect("..")


@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    form = VoucherForm  # ← integrated here
    form = VoucherAdminForm
    list_display = ('code', 'business', 'duration_minutes',
                    'expires_at', 'is_active')
    list_filter = ('business', 'is_active')
    search_fields = ('code', 'business__name')
    autocomplete_fields = ['business', 'created_by']
    readonly_fields = ('created_at', 'usage_count', 'usage_limit')
    actions = [export_vouchers_csv]


@admin.register(VoucherUsage)
class VoucherUsageAdmin(admin.ModelAdmin):
    list_display = (
        'voucher', 'mac_address', 'user',
        'used_at', 'session_duration'
    )
    list_filter = ('used_at', 'voucher__business')
    search_fields = ('voucher__code', 'user__username', 'mac_address')
    autocomplete_fields = ['voucher', 'user', 'session_duration']
    readonly_fields = ('used_at',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        self._business_voucher_counts = dict(
            qs.values('business_id').annotate(count=models.Count('id'))
        )
        return qs

    def quota_status(self, obj):
        current = self._business_voucher_counts.get(obj.business_id, 0)
        quota = getattr(obj.business, 'voucher_quota', 100)
        return f"{current}/{quota}"

    quota_status.short_description = "Quota Usage"
    list_display += ('quota_status',)


@admin.register(VoucherGenerationLog)
class VoucherGenerationLogAdmin(admin.ModelAdmin):
    list_display = ('business', 'count', 'prefix', 'created_by', 'created_at')
    list_filter = ('business', 'created_at')
    search_fields = ('business__name', 'created_by__username')
    autocomplete_fields = ['business', 'created_by']
    readonly_fields = ('count', 'created_at')
