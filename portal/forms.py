from django import forms


class VoucherLoginForm(forms.Form):
    voucher_code = forms.CharField(label="Voucher Code", max_length=100)
    ip_address = forms.GenericIPAddressField(label="Your IP Address")
    mac_address = forms.CharField(label="Your MAC Address", max_length=17)

    def clean_mac_address(self):
        mac = self.cleaned_data["mac_address"]
        return mac.lower().replace("-", ":")  # normalize MAC
