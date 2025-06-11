from django.contrib import admin
from .models import PaymentTransaction


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'phone_number',
                    'amount', 'status', 'timestamp')
    list_filter = ('status',)
    search_fields = ('transaction_id', 'phone_number')
    ordering = ('-timestamp',)
