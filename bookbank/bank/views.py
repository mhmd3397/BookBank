from django.shortcuts import render, redirect

# Create your views here.


def main_page(request):
    return render(request, "main_page.html")


def employee_registration_view(request):
    return render(request, "employee_register.html")


def customer_registration_view(request):
    return render(request, 'customer_register.html')


def login(request):
    return render(request, 'login_page.html')

def logout(request):
    pass
    return redirect('/')