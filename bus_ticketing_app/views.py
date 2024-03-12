from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Passenger, Driver
from django.contrib.auth.hashers import make_password

# Create your views here.
# Displaying the views
def indexView(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    return render(request, "bus_ticketing_app/layout.html", {
        "user": user
    })

def adminView(request):
    return render(request, "bus_ticketing_app/Admin/adminLogin.html")

def driverLoginView(request):
    return render(request, "bus_ticketing_app/drivers/loginD.html")


def passengerLoginView(request):
    return render(request, "bus_ticketing_app/users/index.html")

def driverSignUpView(request):
    return render(request, "bus_ticketing_app/drivers/index.html")

# User Sign Up Validation
def userSignUp(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        password = request.POST.get('password')
        
        # Validate fields
        if not(name and email and phone_number and address and password):
            return render(request, "bus_ticketing_app/users/index.html", {
                "message": "All Fields Are Required"
            })
        
        #checks if phone number already exist
        if Passenger.objects.filter(phone_number=phone_number).exists():
            return render(request, "bus_ticketing_app/users/index.html", {
                "message": "Phone Number Aready Exists"
            })
        #checks if email already exist
        if Passenger.objects.filter(email=email).exists():
            return render(request, "bus_ticketing_app/users/index.html", {
                "message": "Email Adress already exists"
            })
        
        # Harsh Password
        hashed_password = make_password(password)

        # Create and save the user
        user = Passenger(name=name, email=email, phone_number=phone_number, address=address, password=hashed_password)
        user.save()
        return render(request, "bus_ticketing_app/users/user_home.html")
    else:
        return HttpResponse("failed")
    
def userSignIn(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("Success")
        else:
            return HttpResponse("invalid username or password")
    else:
        return HttpResponse("failed")



def driverSignUp(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        comfirm_password = request.POST.get('comfirm_password')
        
        # Validate fields
        if not(name and username and email and phone_number and password and comfirm_password):
            message = "All fields are required"
            return render(request, "bus_ticketing_app/drivers/index.html", {
                    "message": message
            })
        
        if password != comfirm_password:
            message = "Password does not match"
            return redirect("bus_ticketing_app:driversignup")
        
        #checks if phone number already exist
        if Driver.objects.filter(phone_number=phone_number).exists():
            return render(request, "bus_ticketing_app/drivers/index.html", {
                "message": "Phone Number Aready Exists"
            })
        #checks if email already exist
        if Driver.objects.filter(email=email).exists():
            return render(request, "bus_ticketing_app/drivers/index.html", {
                "message": "Email Adress already exists"
            })
        
        # Harsh Password
        hashed_password = (make_password(password), make_password(comfirm_password))

        # Create and save the user
        driver = Driver(name=name, username=username, email=email, phone_number=phone_number, password=hashed_password, comfirm_password=hashed_password)
        driver.save()
        return HttpResponse("success")
    else:
        return HttpResponse("failed")

def driverLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        hashed_password = make_password(password)
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("Login Successful")
        else:
            return HttpResponse("invalid credentials")
    else:
        return HttpResponse("failed")

def book(request):
    return render(request, "bus_ticketing_app/users/book.html", {
            "Message": "`you did'nt sign up"
        })

def driverLogout(request):
    logout(request)

def userLogOut(request):
    logout(request)