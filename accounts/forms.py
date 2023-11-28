# accounts/forms.py
from django import forms
from .models import Patient, Doctor, Admin, Appointment, Products

class CommonRegistrationForm(forms.ModelForm):
    class Meta:
        model = Patient  # Use Patient as a placeholder; it will be dynamically changed in views
        fields = ['email', 'firstname', 'lastname', 'password']

class PatientRegistrationForm(CommonRegistrationForm):
    class Meta(CommonRegistrationForm.Meta):
        model = Patient

class DoctorRegistrationForm(CommonRegistrationForm):
    class Meta(CommonRegistrationForm.Meta):
        model = Doctor

class AdminRegistrationForm(CommonRegistrationForm):
    class Meta(CommonRegistrationForm.Meta):
        model = Admin

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'email', 'phone', 'date', 'department', 'message']

class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'price', 'description', 'origin', 'color']

