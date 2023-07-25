from django.db import models
from datetime import date, datetime
import re
import bcrypt


class UserManager(models.Manager):
    def basic_validator_registration(self, postData):
        errors = {}
        # Validate First Name
        first_name = postData.get('first_name')
        if not first_name:
            errors['first_name'] = "First name is required."
        elif len(first_name) < 2:
            errors['first_name'] = "First name should be at least 2 characters." 
        # Validate Last Name
        last_name = postData.get('last_name')
        if not last_name:
            errors['last_name'] = "Last name is required."
        elif len(last_name) < 2:
            errors['last_name'] = "Last name should be at least 2 characters."
        # Validate Email
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        email = postData.get('email')
        if not email:
            errors['email'] = "Email is required."
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email format."
        else:
            # Check if a user with the same email already exists
            existing_user = User.objects.filter(email=email).first()
            if existing_user:
                errors['email'] = "A user with this email already exists."
        # Validate Password
        password = postData.get('password')
        confirm_password = postData.get('confirm_password')
        if not password:
            errors['password'] = "Password is required."
        elif len(password) < 8:
            errors['password'] = "Password should be at least 8 characters."
        elif password != confirm_password:
            errors['confirm_password'] = "Passwords do not match."
        return errors


class EmployeeManager(models.Manager):
    def basic_validator_registration(self, postData):
        errors = {}
        # Validate First Name
        first_name = postData.get('first_name')
        if not first_name:
            errors['first_name'] = "First name is required."
        elif len(first_name) < 2:
            errors['first_name'] = "First name should be at least 2 characters."  # noqa
        # Validate Last Name
        last_name = postData.get('last_name')
        if not last_name:
            errors['last_name'] = "Last name is required."
        elif len(last_name) < 2:
            errors['last_name'] = "Last name should be at least 2 characters."
        # Validate Email
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        email = postData.get('email')
        if not email:
            errors['email'] = "Email is required."
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email format."
        else:
            # Check if a user with the same email already exists
            existing_user = User.objects.filter(email=email).first()
            if existing_user:
                errors['email'] = "A user with this email already exists."
        # Validate Password
        password = postData.get('password')
        confirm_password = postData.get('confirm_password')
        if not password:
            errors['password'] = "Password is required."
        elif len(password) < 8:
            errors['password'] = "Password should be at least 8 characters."
        elif password != confirm_password:
            errors['confirm_password'] = "Passwords do not match."
        # validate Employee_id
        employee_id_REGEX = re.compile(r"^[A-Z\d]{1}[A-Z\d._/\-]{49}$")
        employee_id = postData.get('employee_id')
        if not employee_id:
            errors['employee_id'] = "employee id is required."
        elif not employee_id_REGEX.match(postData['employee_id']):
            errors['employee_id'] = "Invalid employee id."
        return errors

    def basic_validator_login(self, postData):
        errors = {}
        # Validate Email
        email = postData.get('email')
        existing_user = User.objects.filter(email=email).first()
        existing_Employee = Employee.objects.filter(email=email).first()
        if not existing_user:
            if not existing_Employee:
                errors['email'] = "Your email or password is incorrect."
        # Validate password
        user = User.objects.filter(email=email)
        employee = Employee.objects.filter(email=email)
        if user:
            logged_user = user[0]
            if not bcrypt.checkpw(postData.get('password').encode(), logged_user.password.encode()):  # noqa
                errors['password'] = "Your email or password is incorrect."
        if employee:
            logged_employee = employee[0]
            if not bcrypt.checkpw(postData.get('password').encode(), logged_employee.password.encode()):  # noqa
                errors['password'] = "Your email or password is incorrect."
        return errors

class AppointmentManager(models.Manager):
    def basic_validator_appointment(self, postData):
        errors = {}
        # Validate Day
        day = postData.get('day')
        if not day:
            errors['day'] = "Day Feild is required."
        if day:
            try:
                day_date = datetime.strptime(day, '%Y-%m-%d').date()
                today = date.today()
                if (today - day_date).days > 0:
                    errors['day'] = "Appointment cannot be in the Past."
            except ValueError:
                errors['day'] = "Invalid date format."
        return errors


# Create your models here.
TIME_CHOICES = (
    ("8:30 AM", "8:30 AM"),
    ("9 AM", "9 AM"),
    ("9:30 AM", "9:30 AM"),
    ("10 AM", "10 AM"),
    ("10:30 AM", "10:30 AM"),
    ("11 AM", "11 AM"),
    ("11:30 AM", "11:30 AM"),
    ("12 PM", "12 PM"),
    ("12:30 PM", "12:30 PM"),
    ("1 PM", "1 PM"),
    ("1:30 PM", "1:30 PM"),
    ("2 PM", "2 PM"),
)

SERVICES_CHOICES = (
    ("Teller", "Teller"),
    ("Customer service", "Customer service")
)


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()


class Employee(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    employee_id = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = EmployeeManager()


class Appointment(models.Model):
    day = models.DateField()
    # default needs to be added for time choices
    time = models.CharField(max_length=255, choices=TIME_CHOICES)
    service_type = models.CharField(
        max_length=255, choices=SERVICES_CHOICES, default="Teller")
    user = models.ForeignKey(User, related_name="users",
                             on_delete=models.CASCADE)
    employee = models.ForeignKey(
        Employee, related_name="employees", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AppointmentManager()
