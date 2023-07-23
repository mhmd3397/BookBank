from django.shortcuts import render, redirect
from .models import User, Employee, Appointment

# Create your views here.


def main_page(request):
    return render(request, "main_page.html")


def employee_registration_view(request):
    return render(request, "employee_register.html")


def customer_registration_view(request):
    return render(request, 'customer_register.html')


def login(request):
    return render(request, 'login_page.html')


def home_page_customer(request):
    # context = {
    #     'user': request.session['user'],
    #     'message': request.session['message']
    # }
    # #this can be updated after implementing the other methods
    return render(request, 'home_page_customer.html', ) #context needs to be added


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


from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def page_view(request):
    user = request.user
    appointments = user.appointment_set.all() 
    return render(request, 'page.html', {'user': user, 'appointments': appointments})
