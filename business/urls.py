from django.urls import path
from . import views

app_name = 'business'

urlpatterns = [
    path('dashboard/', views.business_dashboard, name='dashboard'),
    path('vouchers/', views.my_voucher_list, name='voucher_list'),
    path('vouchers/generate/', views.generate_vouchers_view,
         name='generate_vouchers'),
    path('vouchers/generated/', views.view_generated_vouchers,
         name='view_generated_vouchers'),
    path('profile/edit/', views.edit_business_profile, name='edit_profile'),
    path('usage/', views.usage_stats_view, name='usage_stats'),
    #     path('select/', views.select_business, name='select_business'),

]
