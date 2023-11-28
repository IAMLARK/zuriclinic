from django.contrib import admin
from django.urls import path
from accounts import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('patient_index', views.patient_index, name='patient_index'),
    path('doctor_index', views.doctor_index, name='doctor_index'),
    path('admin_index', views.admin_index, name='admin_index'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('departments/', views.departments, name='departments'),
    path('doctors/', views.doctors, name='doctors'),
    path('contacts/', views.contacts, name='contacts'),
    path('register/', views.register_user, name='register_user'),
    path('login/<str:user_type>/', views.login_user, name='login_user'),

    path('patient/', views.register_user, {'user_type': 'patient'}, name='register_patient'),
    path('doctor/', views.register_user, {'user_type': 'doctor'}, name='register_doctor'),
    path('admin/', views.register_user, {'user_type': 'admin'}, name='register_admin'),
    path('login/patient/', views.login_user, {'user_type': 'patient'}, name='login_patient'),
    path('login/doctor/', views.login_user, {'user_type': 'doctor'}, name='login_doctor'),
    path('login/admin/', views.login_user, {'user_type': 'admin'}, name='login_admin'),
    path('book_appointment/', views.book_appointment, name='book_appointment'),
    path('view_appointment/', views.view_appointment, name='view_appointment'),

    path('add/', views.add, name='add'),
    path('show/', views.show, name='show'),
    path('show1/', views.show1, name='show1'),
    path('/delete/<int:id>', views.delete),
    path('/edit/<int:id>', views.edit),
    path('/update/<int:id>', views.update),
    path('pay/', views.pay, name='pay'),
    path('token/', views.token, name='token'),
    path('stk/', views.stk, name='stk'),

]
