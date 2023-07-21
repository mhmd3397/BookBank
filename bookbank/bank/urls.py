from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page),
    path('employee_registration/', views.employee_registration_view,
         name='employee_registration'),
    path('customer_registration/', views.customer_registration_view,
         name='customer_registration'),
    path('login_page/', views.login,
         name='login_registration'),
]
