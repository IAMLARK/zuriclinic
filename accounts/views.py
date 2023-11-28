import json

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PatientRegistrationForm, DoctorRegistrationForm, AdminRegistrationForm, AppointmentForm, ProductsForm
from .models import Appointment, Products
import requests
from django.http import HttpResponse
from requests.auth import HTTPBasicAuth
from accounts.credentials import MpesaC2bCredential, MpesaAccessToken, LipanaMpesaPpassword

# Create your views here.

def register_user(request, user_type):
    if user_type == 'patient':
        form_class = PatientRegistrationForm
    elif user_type == 'doctor':
        form_class = DoctorRegistrationForm
    elif user_type == 'admin':
        form_class = AdminRegistrationForm
    else:
        # Handle invalid user type
        return redirect('index')

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(f'{user_type}_index')  # Redirect to the specific dashboard
    else:
        form = form_class()

    return render(request, 'registration.html', {'form': form})

def login_user(request, user_type):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)

            if user_type == 'patient':
                return redirect('patient_index')
            elif user_type == 'doctor':
                return redirect('doctor_index')
            elif user_type == 'admin':
                return redirect('admin_index')
            else:
                return redirect('index')  # Redirect to a default page if user_type is not recognized
        else:
            messages.error(request, 'Invalid credentials. Please try again.')

    return render(request, 'login.html', {'user_type': user_type})





def index(request):
    return render(request, template_name='index.html')

def about(request):
    return render(request, template_name='about.html')
def services(request):
    return render(request, template_name='services.html')

def departments(request):
    return render(request, template_name='departments.html')

def doctors(request):
    return render(request, template_name='doctors.html')
def contacts(request):
    return render(request, template_name='contacts.html')
@login_required
def patient_index(request):
    return render(request, 'patient_index.html', {'welcome_message': f'Welcome {request.user.firstname}'})


@login_required
def doctor_index(request):
    return render(request, 'doctor_index.html', {'welcome_message': f'Welcome {request.user.firstname}'})

@login_required
def admin_index(request):
    return render(request, 'admin_index.html', {'welcome_message': f'Welcome {request.user.firstname}'})

@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.save()
            return redirect('patient_index')
    else:
        form = AppointmentForm()

    return render(request, 'book_appointment.html', {'form': form})

@login_required
def view_appointment(request, appointment_id):
    appointment = Appointment.objects.get(pk=appointment_id)
    return render(request, 'view_appointment.html', {'appointment': appointment})

def add(request):
    if request.method == "POST":
        form = ProductsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
            form = ProductsForm()
            return render(request, template_name='addproduct.html', context={'form': form})

def show(request):
    products = Products.objects.all()
    return render(request, template_name='show.html', context={'products': products})

def show1(request):
    products = Products.objects.all()
    return render(request, template_name='show1.html', context={'products': products})


def delete(request, id):
    product = Products.objects.get(id=id)
    product.delete()
    return redirect('/show')

def edit(request, id):
    product = Products.objects.get(id=id)
    return render(request, template_name='edit.html', context={'product': product})


def update(request, id):
    product = Products.objects.get(id=id)
    form = ProductsForm(request.POST, instance=product)
    if form.is_valid():
        form.save()
        return redirect('/show')
    else:
        return render(request, template_name='edit.html', context={'product': product})

def pay(request):
    return render(request, template_name='pay.html')

def token(request):
    consumer_key = 'MCc2zOlbXCrvpX5HuQ4GyKn6dOaAY35G'
    consumer_secret = 'kwijBjvDKPO7CvTG'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token": validated_mpesa_access_token})

def stk(request):
    if request.method == "POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "Lark Enterprise",
            "TransactionDesc": "Web Development Charges"
        }
        response = requests.post(api_url, json=request, headers=headers)
        return HttpResponse('success')