from django.shortcuts import render, redirect
from .models import User, Employee, Appointment, SERVICES_CHOICES, TIME_CHOICES
from django.contrib import messages
from django.http import JsonResponse
import bcrypt

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
        else:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            employee_id = request.POST['employee_id']
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(
                password.encode(), bcrypt.gensalt()).decode()
            Employee.objects.create(first_name=first_name, last_name=last_name,
                                    email=email, employee_id=employee_id, password=pw_hash)  # noqa
            request.session['employee'] = first_name + " " + last_name
            context = {  # noqa
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
        else:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(
                password.encode(), bcrypt.gensalt()).decode()
            User.objects.create(first_name=first_name,
                                last_name=last_name, email=email, password=pw_hash)  # noqa
            request.session['message'] = "You have registered successfully"
            request.session['user'] = User.objects.get(email=email)
            context = {  # noqa
                'message': request.session['message']
            }
            return redirect('home_page_customer')
    return render(request, 'customer_register.html')


def login(request):
    if 'user' in request.session:
        return redirect('home')
    if 'employee' in request.session:
        return redirect('home')
    if request.method == 'POST':
        errors = Employee.objects.basic_validator_login(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('login_registration')
        email = request.POST['email']
        print(email)
        user = User.objects.filter(email=email).first()
        employee = Employee.objects.filter(email=email).first()
        request.session['message'] = "You have logged in successfully"
        request.session['email'] = email
        if user:
            request.session['user'] = {
                'first_name': user.first_name,
                'user_id': user.id
            }
            return redirect('home')
        elif employee:
            request.session['employee'] = {
                'first_name': employee.first_name
            }
            return redirect('home')
    return render(request, 'login_page.html')


def home_page_customer(request):
    if 'user' not in request.session:
        return redirect('home')
    if 'employee' in request.session:
        return redirect('home')
    message = request.session.get('message')
    email = request.session.get('email')
    users = User.objects.filter(email=email)
    appointments = Appointment.objects.all()
    return render(request, 'home_page_customer.html', {'message': message, 'users': users, 'appointments': appointments})  # noqa


def home_page_employee(request):
    if 'user' in request.session:
        return redirect('home')
    if 'employee' not in request.session:
        return redirect('home')
    message = request.session.get('message')
    employee = request.session.get('employee')
    return render(request, 'home_page_employee.html', {'message': message, 'employee': employee})  # noqa


def all_appointments(request):
    if 'user' in request.session:
        return redirect('home_page_customer')
    if 'employee' not in request.session:
        return redirect('home')

    service_type = None
    appointments = Appointment.objects.all()

    if request.method == 'POST':
        if 'Teller' in request.POST:
            appointments = Appointment.objects.filter(service_type='Teller')
            service_type = "Teller"
        else:
            appointments = Appointment.objects.filter(
                service_type='Customer service')
            service_type = "Customer service"

    return render(request, 'all_appointment.html', {'appointments': appointments, 'service_type': service_type})


def appointment_details(request, id):
    try:
        appointment = Appointment.objects.get(id=id)
        appointment_data = {
            'service_type': appointment.service_type,
            'day': appointment.day,
            'time': appointment.time,
            # Add other appointment details as needed
        }
        return JsonResponse(appointment_data)
    except Appointment.DoesNotExist:
        return JsonResponse({'error': 'Appointment not found.'}, status=404)


def create_appointment(request):
    if 'user' not in request.session:
        return redirect('home')
    if 'employee' in request.session:
        return redirect('home')

    service_choices = SERVICES_CHOICES
    time_choices = TIME_CHOICES

    if request.method == 'POST':
        errors = Appointment.objects.basic_validator_appointment(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('create_appointment')
        else:
            email = request.session.get('email')
            user = User.objects.get(email=email)
            print(user.id)
            Appointment.objects.create(
                day=request.POST.get('appointment_day'),
                service_type=request.POST.get('service_type'),
                time=request.POST.get('time'),
                user=User.objects.get(id=user.id)
            )
            return redirect('home_page_customer')

    return render(request, 'creating_appointment_page.html', {'service_choices': service_choices, 'time_choices': time_choices})


def edit(request, id):
    # get the appointment from the database using the id
    return render(request, "edit.html")


def delete(request, id):
    try:
        appointment = Appointment.objects.get(id=id)
        appointment.delete()
        return JsonResponse({'message': 'Appointment deleted successfully.'})
    except Appointment.DoesNotExist:
        return JsonResponse({'error': 'Appointment not found.'}, status=404)


# def delete(request, id):
#     # appointment = Appointment.objects.get(id=id)
#     # appointment.delete()
#     return redirect('home_page_customer')


def logout(request):
    request.session.flush()
    return redirect('home')


def get_available_time_slots(request):
    if request.method == 'GET':
        selected_day = request.GET.get('day')
        selected_service_type = request.GET.get('service_type')

        # Fetch the existing appointments for the selected day and service type
        existing_appointments = Appointment.objects.filter(
            day=selected_day, service_type=selected_service_type).values_list('time', flat=True)

        # Get all time choices as a list
        all_time_choices = [choice[0] for choice in TIME_CHOICES]

        # Filter out the already taken time slots from all time choices
        available_time_slots = sorted(
            list(set(all_time_choices) - set(existing_appointments)))

        return JsonResponse({'available_time_slots': available_time_slots})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
