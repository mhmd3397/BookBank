from django.db import models
from datetime import date, datetime
import re
import bcrypt


def calculate_age(born):
    today = date.today()
    return today.year-born.year-((today.month, today.day) < (born.month, born.day))  # noqa


class UserManager(models.Manager):
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
        # Validate Birthday (if provided)
        birthday = postData.get('birthday')
        if birthday:
            try:
                birthday_date = datetime.strptime(birthday, '%Y-%m-%d').date()
                today = date.today()
                if (today - birthday_date).days < 0:
                    errors['birthday'] = "Birthday cannot be in the future."
                elif calculate_age(birthday_date) < 13:
                    errors['birthday'] = "You must be at least 13 years old to register."  # noqa
            except ValueError:
                errors['birthday'] = "Invalid date format."
        return errors

    def basic_validator_login(self, postData):
        errors = {}
        # Validate Email
        email = postData.get('email')
        existing_user = User.objects.filter(email=email).first()
        if not existing_user:
            errors['email'] = "A user not found."
        # Validate password
        user = User.objects.filter(email=email)
        if user:
            logged_user = user[0]
            if not bcrypt.checkpw(postData.get('password').encode(), logged_user.password.encode()):  # noqa
                errors['password'] = "Your password is incorrect."
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
    ("2:30 PM", "2:30 PM"),
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


class Employee(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    employee_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Appointment(models.Model):
    day = models.DateField()
    # default needs to be added
    time = models.CharField(max_length=255, choices=TIME_CHOICES)
    service_type = models.CharField(
        max_length=255, choices=SERVICES_CHOICES, default="Teller")
    user = models.ForeignKey(User, related_name="users",
                             on_delete=models.CASCADE)
    employee = models.ForeignKey(
        Employee, related_name="employees", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
