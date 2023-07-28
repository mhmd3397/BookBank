from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='home'),
    path('employee_registration/', views.employee_registration_view,
         name='employee_registration'),
    path('customer_registration/', views.customer_registration_view,
         name='customer_registration'),
    path('login_page/', views.login, name='login_registration'),
    path('home_page_customer/', views.home_page_customer,
         name='home_page_customer'),
    path('home_page_employee/', views.home_page_employee,
         name='home_page_employee'),
    path('appointment_detail/<int:id>/',
         views.appointment_details, name='appointment_details'),
    path('all_appointments/', views.all_appointments, name='all_appointments'),
    path('all_appointments/<int:id>/',
         views.appointment_details, name='appointment_details'),
    path('create_appointment/', views.create_appointment,
         name='create_appointment'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('logout/', views.logout, name='logout'),
    path('get_available_time_slots/', views.get_available_time_slots,
         name='get_available_time_slots'),

]
