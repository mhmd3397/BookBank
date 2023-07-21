from django.shortcuts import render, redirect

# Create your views here.


def main_page(request):
    return render(request, "main_page.html")


def staff_registration_view(request):
    return render(request, 'staff_registration.html')


def customer_registration_view(request):
    return render(request, 'customer_registration.html')
