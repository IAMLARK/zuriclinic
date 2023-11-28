from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=20)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    # Add any other required fields for authentication

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class Patient(CustomUser):
    # Add any additional fields specific to the Patient model

    def save(self, *args, **kwargs):
        # Add any additional logic needed when saving a Patient
        super().save(*args, **kwargs)

class Doctor(CustomUser):
    # Add any additional fields specific to the Doctor model

    def save(self, *args, **kwargs):
        # Add any additional logic needed when saving a Doctor
        super().save(*args, **kwargs)

class Admin(CustomUser):
    # Add any additional fields specific to the Admin model

    def save(self, *args, **kwargs):
        # Add any additional logic needed when saving an Admin
        super().save(*args, **kwargs)

class Appointment(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date = models.DateField()
    department = models.CharField(max_length=255)
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name + " " + self.email

class Products(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    description = models.TextField()
    origin = models.CharField(max_length=50, default="Kenya")
    color = models.CharField(max_length=50, default="white")

    def __str__(self):
        return self.name