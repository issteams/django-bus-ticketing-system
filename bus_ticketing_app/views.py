from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Passenger, Driver, BusRoute
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime, timedelta
from bus_ticketing_app.CustomUserBackEnd import CustomUserBackend

# Create your views here.
# Displaying the views
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

def bus_route(request):
    return render(request, "bus_ticketing_app/users/bus_route.html")

def bus_reserve(request):
    return render(request, "bus_ticketing_app/users/reserve.html")

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
        
        # Check if phone number already exists
        if Passenger.objects.filter(phone_number=phone_number).exists():
            return render(request, "bus_ticketing_app/users/index.html", {
                "message": "Phone Number Already Exists"
            })
        # Check if email already exists
        if Passenger.objects.filter(email=email).exists():
            return render(request, "bus_ticketing_app/users/index.html", {
                "message": "Email Address Already Exists"
            })
        
        # Hash Password
        hashed_password = make_password(password)

        # Create and save the user
        user = Passenger(name=name, email=email, phone_number=phone_number, address=address, password=hashed_password)
        user.save()
        return redirect("bus_ticketing_app:user_home")
    else:
        return HttpResponse("failed")

def userSignIn(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = CustomUserBackend.authenticate(request, username=username, password=password)
            if check_password(password, user.password):
                login(request, user)
                return redirect("bus_ticketing_app:user_home")
            else:
                return HttpResponse("Invalid Username or Password")
        except Passenger.DoesNotExist:
            return HttpResponse("Invalid Username or Password")
    else:
        return HttpResponse("failed")

def driverSignUp(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validate fields
        if not(name and username and email and phone_number and password and confirm_password):
            message = "All fields are required"
            return render(request, "bus_ticketing_app/drivers/index.html", {
                    "message": message
            })
        
        if password != confirm_password:
            message = "Password does not match"
            return redirect("bus_ticketing_app:driversignup")
        
        # Check if phone number already exists
        if Driver.objects.filter(phone_number=phone_number).exists():
            return render(request, "bus_ticketing_app/drivers/index.html", {
                "message": "Phone Number Already Exists"
            })
        # Check if email already exists
        if Driver.objects.filter(email=email).exists():
            return render(request, "bus_ticketing_app/drivers/index.html", {
                "message": "Email Address Already Exists"
            })
        
        # Hash Password
        hashed_password = make_password(password)

        # Create and save the driver
        driver = Driver(name=name, username=username, email=email, phone_number=phone_number, password=hashed_password)
        driver.save()
        return HttpResponse("Success")
    else:
        return HttpResponse("Failed")

def driverLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("Login Successful")
        else:
            return HttpResponse("Invalid Credentials")
    else:
        return HttpResponse("Failed")

def book(request):
    return render(request, "bus_ticketing_app/users/book.html", {
            "Message": "`You didn't sign up"
        })

def search_bus_route(request):
    origin = request.GET.get('origin')
    destination = request.GET.get('destination')
    date = request.GET.get('date')
    
    if origin and destination and date:
        # Filter bus routes within the date range
        bus_routes = BusRoute.objects.filter(origin=origin, destination=destination, date=date)
        
        if bus_routes.exists():
            response = ""
            for route in bus_routes:
                response += f"From {route.origin} to {route.destination} on {route.date}<br>Departure time {route.departure_time}<br>Arrival time {route.arrival_time}<br>Total seats {route.total_seats}<br>Available Seats {route.available_seats}"
            return HttpResponse(response)
        else:
            return HttpResponse("No bus routes found for the given criteria.")
    else:
        return HttpResponse("Please provide origin, destination, and date parameters.")

def reserve(request):
    if request.method == 'GET':
        # Retrieve user and bus routes
        user = request.user
        bus_routes = BusRoute.objects.all()
        
        # Render the reservation form template with user and bus route data
        return render(request, 'bus_ticketing_app/users/reserve.html', {'user': user, 'bus_routes': bus_routes })
    
    elif request.method == 'POST':
        # Get form data from POST request
        user = request.POST.get('full_name')
        bus_route_id = request.POST.get('bus_route')
        seat_number = request.POST.get('seat_number')

        # Validate and process the reservation
        if user and bus_route_id and seat_number:
            try:
                bus_route = BusRoute.objects.get(id=bus_route_id)
                # Check if the seat is available
                if bus_route.available_seats >= int(seat_number):
                    # You should implement your logic to check seat availability here
                    # For example, you could check if the seat is not already booked for the selected route
                    # If the seat is available, create a new booking
                    booking = Book.objects.create(user=user, bus_route=bus_route, seat_number=seat_number)
                    # Optionally, you can redirect to a success page or display a success message
                    return HttpResponse('Booking Success')
                else:
                    return HttpResponse('Requested seats are not available')
            except BusRoute.DoesNotExist:
                return render(request, 'bus_ticketing_app/users/error.html', {'error_message': 'Bus route does not exist.'})
        else:
            return render(request, 'bus_ticketing_app/users/error.html', {'error_message': 'Invalid form data.'})
    else:
        return render(request, 'bus_ticketing_app/users/error.html', {'error_message': 'Invalid request method.'})

def user_home(request):
    if not request.user.is_authenticated:
        return redirect("bus_ticketing_app:index")
    else:
        return render(request, "bus_ticketing_app/users/user_home.html")

def driverLogout(request):
    logout(request)

def userLogOut(request):
    logout(request)
    return redirect("bus_ticketing_app:index")
