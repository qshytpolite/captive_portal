"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__reload__/', include('django_browser_reload.urls')),

    # Accounts
    path('accounts/', include('accounts.urls')),

    # Core
    # path('', include('core.urls')),

    # Business
    path('business/', include('business.urls')),
    # path('business/', include(('business.urls', 'business'))),

    # Portal
    path('', include('portal.urls')),

    # Voucher
    path('api/voucher/', include('voucher.urls')),

    # Payments
    path('api/payments/', include('payments.urls')),

    # Router API
    path('api/routerapi/', include('routerapi.urls')),
]
