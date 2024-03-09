from . import views
from django.urls import path

app_name = 'bus_ticketing_app'
urlpatterns = [
    path('', views.indexView, name='index'),
    path('admin/login/', views.adminView, name='adminlogin'),
    path("driver/login/", views.driverLoginView, name='driverlogin'),
    path("passenger/login/", views.passengerLoginView, name='passengerlogin'),
    path("driver/signup/", views.driverSignUpView, name='driversignup'),
    path("welcome/", views.userSignUp, name='userSignUp'),
    path("welcome_back/", views.userSignIn, name='userSignIn'),
]