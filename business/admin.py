from django import forms
from django.contrib import admin, messages
from .models import (
    Business,
    BusinessMembership,
    SubscriptionPlan,
    BusinessSubscription
)
from voucher.services import create_vouchers
from .forms import BusinessMemberForm
from routerapi.models import RouterConfig
from voucher.models import Voucher

# Step 1: Define the form used in the admin action


class VoucherGenerationForm(forms.Form):
    count = forms.IntegerField(min_value=1, max_value=500, initial=10)
    prefix = forms.CharField(max_length=20, initial="HOTSPOT")
    duration_minutes = forms.IntegerField(min_value=5, initial=60)

# edit RouterConfig in admin


class RouterConfigInline(admin.StackedInline):
    model = RouterConfig
    extra = 0


class VoucherInline(admin.TabularInline):  # or StackedInline if more fields
    model = Voucher
    extra = 0
    readonly_fields = ('code', 'created_at', 'expires_at')
    can_delete = False
    show_change_link = True


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    inlines = [RouterConfigInline, VoucherInline]
    list_display = ('name', 'owner', 'is_active', 'created_at')
    search_fields = ('name', 'owner__username')
    list_filter = ('is_active', 'created_at')
    autocomplete_fields = ['owner']
    actions = ['generate_default_vouchers']
    action_form = VoucherGenerationForm

    def generate_vouchers_for_business(self, request, queryset):
        form = self.get_action_form(request)

        if not form.is_valid():
            self.message_user(request, "Invalid input", level=messages.ERROR)
            return

        count = form.cleaned_data["count"]
        prefix = form.cleaned_data["prefix"]
        # 1 day = 1440 minutes
        duration_minutes = form.cleaned_data["duration_minutes"]

        for business in queryset:
            create_vouchers(
                business=business,
                count=count,
                prefix=prefix,
                duration_minutes=duration_minutes,
                created_by=request.user
            )

        self.message_user(
            request,
            f"Successfully generated {count} vouchers per selected business.",
            level=messages.SUCCESS
        )

    generate_vouchers_for_business.short_description = "Generate vouchers for selected business(es)"


@admin.register(BusinessMembership)
class BusinessMembershipAdmin(admin.ModelAdmin):
    form = BusinessMemberForm
    list_display = ('user', 'business', 'role', 'joined_at')
    list_filter = ('role', 'joined_at')
    search_fields = ('user__username', 'business__name')
    autocomplete_fields = ['user', 'business']


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'max_users',
                    'max_vouchers', 'duration_days')
    search_fields = ('name',)
    list_filter = ('duration_days',)


@admin.register(BusinessSubscription)
class BusinessSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('business', 'plan', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('business__name', 'plan__name')
    autocomplete_fields = ['business', 'plan']
