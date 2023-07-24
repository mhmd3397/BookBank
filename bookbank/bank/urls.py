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
    path('home_page_customer/', views.home_page_customer,
         name='home_page_customer'),
    path('appointment_detail/<int:id>', views.appointment_details,
         name='appintment_details'),
    path('edit/<int:id>', views.edit),
    path('delete/<int:id>', views.delete),
    path('logout/', views.logout, name='logout'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('teller_appointments/', views.teller_appointments, name='teller_appointments'),
    path('customer_appointments/', views.customer_appointments, name='customer_appointments'),
    
]
