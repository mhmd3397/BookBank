from django.shortcuts import render, redirect
from .models import User, Employee, Appointment
from django.contrib import messages
from datetime import datetime, date
import re, bcrypt

# Create your views here.


def main_page(request):
    if 'user' in request.session:
        return redirect('home_page_customer')
    if 'employee' in request.session:
        return redirect('home_page_employee')
    return render(request, "main_page.html")


def employee_registration_view(request):
    if 'user' in request.session:
        return redirect('home_page_customer')
    if 'employee' in request.session:
        return redirect('home_page_employee')
    if request.method == 'POST':
        errors = Employee.objects.basic_validator_registration(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('employee_registration')
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        employee_id = request.POST['employee_id']
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        employee = Employee.objects.create(first_name=first_name, last_name=last_name, email=email, employee_id=employee_id, password=pw_hash)
        request.session['employee'] = first_name + " " + last_name
        context = {
            'employee': request.session['employee']
        }
        return redirect('home_page_employee')
    return render(request, "employee_register.html")


def customer_registration_view(request):
    if 'user' in request.session:
        return redirect('home_page_customer')
    if 'employee' in request.session:
        return redirect('home_page_employee')
    if request.method == 'POST':
        errors = User.objects.basic_validator_registration(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('customer_registration')
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=pw_hash)
        request.session['message'] = "You have registered successfully"
        context = {
            'user': user,
            'message': request.session['message']
        }
        print(user.first_name)
        return redirect('home_page_customer')
    return render(request, 'customer_register.html')


def login(request):
    if 'user' in request.session:
        return redirect('home_page_customer')
    if 'employee' in request.session:
        return redirect('home_page_employee')
    if request.method == 'POST':
        errors = Employee.objects.basic_validator_login(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('login_registration')
        email = request.POST['email']
        user = User.objects.get(email=email)
        employee = Employee.objects.get(email=email)
        request.session['message'] = "You have logged in successfully"
        if user:
            context = {
                'user': user,
                'message': request.session['message']
            }
            redirect('home_page_customer')
        elif employee:
            context = {
                'employee': employee,
                'message': request.session['message']
            }
            redirect('home_page_employee')
    return render(request, 'login_page.html')


def home_page_customer(request):
    if 'user' not in request.session:
        return redirect('home')
    if 'employee' in request.session:
        return redirect('home')
    message = request.session.get('message')
    user = request.session.get('user')
    appointments = user.appointments
    return render(request, 'home_page_customer.html', {'message': message, 'user': user, 'appointments': appointments } )

def home_page_employee(request):
    if 'user' in request.session:
        return redirect('home')
    if 'employee' not in request.session:
        return redirect('home')
    message = request.session.get('message')
    employee = request.session.get('employee')
    return render(request, 'home_page_employee.html', {'message': message, 'employee': employee} )

def all_appointments(request):
    if 'user' in request.session:
        return redirect('home')
    if 'employee' not in request.session:
        return redirect('home')
    appointments = Appointment.objects.all()
    if appointments.service_type == 'Teller':
        appointments = Appointment.objects.filter(service_type = 'Teller')
    else:
        appointments = Appointment.objects.filter(service_type = 'Customer service')
    return render(request, 'all_appointment.html', {'appointments': appointments})

def appointment_details(request, id):
    return render(request, 'home_page_customer.html', )


def edit(request, id):
    #get the appointment from the database using the id
    return render(request, "edit.html")


def delete(request, id):
    # appointment = Appointment.objects.get(id=id)
    # appointment.delete()
    return redirect('home_page_customer')

def logout(request):
    request.session.flush()
    return redirect('home')
