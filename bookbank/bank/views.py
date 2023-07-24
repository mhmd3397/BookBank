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
        print(employee.first_name)
        return redirect('home_page_employee')
    return render(request, "employee_register.html")

    # if 'user' not in request.session:
    #     return redirect('home')
    # if 'employee' in request.session:
    #     return redirect('home')

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
        request.session['user'] = first_name + " " + last_name
        context = {
            'user': request.session['user']
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
        if user:
            context = {
                'user': user
            }
            redirect('home_page_customer')
        elif employee:
            context = {
                'employee': employee
            }
            redirect('home_page_employee')
    return render(request, 'login_page.html')


def home_page_customer(request):
    return render(request, 'home_page_customer.html', )

def home_page_employee(request):
    return render(request, 'home_page_employee.html', )

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
    return redirect('/')
