from django.urls import path
from .views import voucher_login_view
from django.shortcuts import render

urlpatterns = [
    path("login/", voucher_login_view, name="voucher_login"),
    path("success/", lambda r: render(r, "portal/login_success.html"),
         name="login_success"),
]
