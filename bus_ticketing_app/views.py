from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from bus_ticketing_app.EmailBackEnd import EmailBackEnd
from .models import CustomUser, Passenger, Staff
from django.contrib import messages


# Create your views here.
def indexView(request):
    return render(request, "bus_ticketing_app/index.html")

def signin(request):
    return render(request, "bus_ticketing_app/signin.html")

def signup(request):
    return render(request, "bus_ticketing_app/signup.html")


def doLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = EmailBackEnd.authenticate(request, username=email, password=password)
        if user != None:
            login(request, user)
            if user.user_type == '1':
                return redirect('bus_ticketing_app:admin_home')
            elif user.user_type=="2":
                return redirect("bus_ticketing_app:staff_home")
            else:
                return redirect("bus_ticketing_app:user_home")
        else:
            messages.error(request,"Invalid Login Details")
            return redirect("/")

def userSignUp(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        password = request.POST.get('password')

        if not (name and email and phone_number and address and password):
            messages.error(request, "All Fields are required")
            return redirect("bus_ticketing_app:signup")

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email Address Exists")
            return redirect("bus_ticketing_app:signup")

        if Passenger.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "Phone Number Exists")
            return redirect("bus_ticketing_app:signup")
        
        if Staff.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "Phone Number Exists")
            return redirect("bus_ticketing_app:signup")

        # hashed_password = make_password(password)

        user = CustomUser.objects.create_user(username=email, 
                                        first_name=name, 
                                        email=email, 
                                        password=password,
                                        user_type=3
                                        )
        user.passenger.address = address
        user.passenger.phone_number = phone_number
        user.save()
        request.user = user.id
        login(request, user)
        return redirect("bus_ticketing_app:user_home")
    else:
        return HttpResponse("Method not allowed")



def userLogOut(request):
    logout(request)
    return redirect("bus_ticketing_app:index")