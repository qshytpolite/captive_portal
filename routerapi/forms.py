from django import forms
from ipaddress import ip_address
from .models import RouterConfig


class RouterConfigForm(forms.ModelForm):
    class Meta:
        model = RouterConfig
        fields = '__all__'

    def clean_ip_address(self):
        ip_address = self.cleaned_data.get("ip_address")
        try:
            ip_address(ip_address)  # validate IPv4/IPv6 format
        except ValueError:
            raise forms.ValidationError("Enter a valid IP address.")
        return ip_address

    def clean(self):
        cleaned_data = super().clean()
        router_type = cleaned_data.get("router_type")
        ip_address = cleaned_data.get("ip_address")
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        # Example: require credentials for MikroTik routers
        if router_type == "mikrotik":
            if not username or not password:
                raise forms.ValidationError(
                    "Username and password are required for MikroTik routers.")

        if not ip_address:
            raise forms.ValidationError("Router IP address is required.")

        return cleaned_data
