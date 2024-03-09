from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Passenger
from django.contrib.auth.hashers import make_password

# Create your views here.

def indexView(request):
    return render(request, "bus_ticketing_app/index.html")

def adminView(request):
    return render(request, "bus_ticketing_app/Admin/adminLogin.html")

def driverLoginView(request):
    return render(request, "bus_ticketing_app/drivers/loginD.html")


def passengerLoginView(request):
    return render(request, "bus_ticketing_app/users/index.html")

def driverSignUpView(request):
    return render(request, "bus_ticketing_app/drivers/index.html")

def userSignUp(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        password = request.POST.get('password')
        
        # Validate fields
        if not(name and email and phone_number and address and password):
            messages.error(request, "All fields are required")
            return redirect("userSignUp")
        
        #checks if phone number already exist
        if Passenger.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "Phone number already exists")
            return redirect("bus_ticketing_app:userSignUp")

        #checks if email already exist
        if Passenger.objects.filter(email=email).exists():
            messages.error(request, "Email Already exist")
        
        # Harsh Password
        hashed_password = make_password(password)

        # Create and save the user
        user = Passenger(name=name, email=email, phone_number=phone_number, address=address, password=hashed_password)
        user.save()

        messages.success(request, 'Account created successfully')
        return redirect('bus_ticketing_app:userSignIn')
    return HttpResponse("Success")
    
def userSignIn(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("Success")
        else:
            messages.error(request, "invalid username or passsword")
            return redirect("bus_ticketing_app:userSignIn")
    else:
        return HttpResponse("failed")



def validate_signup_data(name, email, phone_number, address, password):
    pass