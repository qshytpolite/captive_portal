from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import Voucher
from business.models import BusinessSubscription
from django.core.exceptions import ValidationError


class VoucherForm(forms.ModelForm):
    class Meta:
        model = Voucher
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        business = cleaned_data.get("business")
        duration_minutes = cleaned_data.get("duration_minutes")
        expires_at = cleaned_data.get("expires_at")

        # Auto-calculate expires_at
        if not expires_at and duration_minutes:
            cleaned_data["expires_at"] = timezone.now(
            ) + timedelta(minutes=duration_minutes)

        # Enforce voucher quota per business subscription plan
        if business:
            try:
                subscription = BusinessSubscription.objects.get(
                    business=business, is_active=True)
                max_allowed = subscription.plan.max_vouchers
                current_active = business.vouchers.filter(
                    is_active=True).count()

                if current_active >= max_allowed:
                    raise forms.ValidationError(
                        f"This business has reached its voucher limit ({max_allowed})."
                    )
            except BusinessSubscription.DoesNotExist:
                raise forms.ValidationError(
                    "Business has no active subscription.")

        return cleaned_data


class VoucherAdminForm(forms.ModelForm):
    class Meta:
        model = Voucher
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        business = cleaned_data.get("business")
        if business:
            active = Voucher.objects.filter(
                business=business, is_active=True).count()
            quota = business.voucher_quota
            if active >= quota:
                raise ValidationError(
                    "This business has reached its voucher quota.")
        return cleaned_data
