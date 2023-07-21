from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page),
    path('staff_registration/', views.staff_registration_view,
         name='staff_registration'),
    path('customer_registration/', views.customer_registration_view,
         name='customer_registration'),
]
