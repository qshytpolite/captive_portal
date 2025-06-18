from django.shortcuts import render, redirect
from .forms import VoucherLoginForm
from voucher.models import Voucher
from business.models import Business
from portal.utils import create_captive_session
from django.contrib import messages
from routerapi.utils import forward_session_to_router


def voucher_login_view(request):
    if request.method == "POST":
        form = VoucherLoginForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["voucher_code"]
            ip = form.cleaned_data["ip_address"]
            mac = form.cleaned_data["mac_address"]

            try:
                voucher = Voucher.objects.select_related(
                    "business").get(code=code)
            except Voucher.DoesNotExist:
                messages.error(request, "Invalid voucher code.")
                return render(request, "portal/voucher_login.html", {"form": form})

            if not voucher.is_valid():
                messages.error(request, "Voucher is expired or invalid.")
                return render(request, "portal/voucher_login.html", {"form": form})

            if not voucher.business.subscription.is_active:
                messages.error(request, "Business subscription inactive.")
                return render(request, "portal/voucher_login.html", {"form": form})

            session = create_captive_session(voucher, ip, mac)
            if not session:
                messages.error(
                    request, "Voucher already in use or invalid device.")
                return render(request, "portal/voucher_login.html", {"form": form})

            forward_session_to_router(session)  # Optional router forwarding
            return redirect("login_success")

    else:
        form = VoucherLoginForm()
    return render(request, "portal/voucher_login.html", {"form": form})
