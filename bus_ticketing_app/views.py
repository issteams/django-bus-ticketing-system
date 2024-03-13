from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Passenger, Driver, BusRoute
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime, timedelta


# Create your views here.
# Displaying the views
def indexView(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    return render(request, "bus_ticketing_app/index.html", {
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

def bus_route(request):
    return render(request, "bus_ticketing_app/users/bus_route.html")


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
        # hashed_password = make_password(password)

        # Create and save the user
        user = Passenger(name=name, email=email, phone_number=phone_number, address=address, password=password)
        user.save()
        return redirect("bus_ticketing_app:user_home")
    else:
        return HttpResponse("failed")
    
def userSignIn(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = Passenger.objects.filter(email=username, password=password)
        if user is not None:
            # login(request, user)
            return redirect("bus_ticketing_app:user_home")
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
        
        # Hash Password
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
        hashed_password = check_password(password)
        user = authenticate(request, username=email, password=hashed_password)
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


def search_bus_route(request):
    origin = request.GET.get('origin')
    destination = request.GET.get('destination')
    date = request.GET.get('date')
    
    if origin and destination and date:
        # Convert the date string to a datetime object
        # try:
        #     date = datetime.strptime(date, "%y-%m-%d")
        # except ValueError:
        #     return HttpResponse("Invalid date format. Please use YYYY-MM-DD.")

        # Define the date range for searching (e.g., +/- 1 day from the specified date)
        # start_date = date - timedelta(days=1)
        # end_date = date + timedelta(days=1)

        # Filter bus routes within the date range
        bus_routes = BusRoute.objects.filter(origin=origin, destination=destination, date=date)
        
        if bus_routes.exists():
            response = ""
            for route in bus_routes:
                response += f"From {route.origin} to {route.destination} on {route.date}<br>"
            return HttpResponse(response)
        else:
            return HttpResponse("No bus routes found for the given criteria.")
    else:
        return HttpResponse("Please provide origin, destination, and date parameters.")


def user_home(request):
    return render(request, "bus_ticketing_app/users/user_home.html")
def driverLogout(request):
    logout(request)

def userLogOut(request):
    logout(request)

    return redirect("bus_ticketing_app:index")