from django import forms
from .models import BusinessMembership


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
