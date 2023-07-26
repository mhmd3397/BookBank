from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='home'),
    path('employee_registration/', views.employee_registration_view,
         name='employee_registration'),
    path('customer_registration/', views.customer_registration_view,
         name='customer_registration'),
    path('login_page/', views.login,
         name='login_registration'),
    path('home_page_customer/', views.home_page_customer,
         name='home_page_customer'),
    path('home_page_employee/', views.home_page_employee,
         name='home_page_employee'),
    path('appointment_detail/<int:id>', views.appointment_details,
         name='appintment_details'),
    path('all_appointments/', views.all_appointments,
         name='all_appointments'),
    path('create_appointment', views.create_appointment,
         name='create_appointment'),
    path('edit/<int:id>', views.edit),
    path('delete/<int:id>', views.delete),
    path('logout/', views.logout, name='logout'),
]
