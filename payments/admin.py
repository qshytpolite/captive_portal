from django.contrib import admin
from .models import PaymentTransaction, WebhookLog, PaymentConfig


@admin.register(PaymentConfig)
class PaymentConfigAdmin(admin.ModelAdmin):
    list_display = ('business', 'provider', 'till_number')
    search_fields = ('business__name', 'till_number')
    autocomplete_fields = ['business']


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'phone_number',
                    'amount', 'status', 'timestamp')
    list_filter = ('status',)
    search_fields = ('transaction_id', 'phone_number')
    ordering = ('-timestamp',)


@admin.register(WebhookLog)
class WebhookLogAdmin(admin.ModelAdmin):
    list_display = ('business', 'event', 'received_at')
    search_fields = ('event', 'business__name')
    list_filter = ('event', 'received_at')
    readonly_fields = ('payload', 'received_at')
    ordering = ('-received_at',)
