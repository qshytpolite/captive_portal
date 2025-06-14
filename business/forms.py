from django import forms
from .models import BusinessMembership, Business


class BusinessProfileForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['name', 'logo', 'business_email',
                  'business_phone', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
        }


class BusinessMemberForm(forms.ModelForm):
    class Meta:
        model = BusinessMembership
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        business = cleaned_data.get('business')
        user = cleaned_data.get('user')

        if role == 'admin':
            # Check if another admin already exists
            existing_admins = BusinessMembership.objects.filter(
                business=business,
                role='admin'
            ).exclude(user=user)

            if existing_admins.exists():
                raise forms.ValidationError(
                    f"{business.name} already has an assigned admin."
                )

        return cleaned_data

# Voucher generation form


class VoucherGenerationForm(forms.Form):
    count = forms.IntegerField(min_value=1, max_value=500, initial=10)
    prefix = forms.CharField(max_length=20, initial="HOTSPOT")
    duration_minutes = forms.IntegerField(
        label='Voucher Duration in (minutes)', min_value=5, initial=60)
