from django.contrib import admin
from .models import Patient, Doctor, Admin, Appointment, Products
# Register your models here.

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Admin)
admin.site.register(Appointment)
admin.site.register(Products)
