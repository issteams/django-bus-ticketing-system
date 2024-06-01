from django.shortcuts import render, redirect
from .models import CustomUser, BusRoute, Passenger, Staff, CustomUser, Bus, Ticket, Schedule, Payment
from django.contrib import messages
from django.http import HttpResponse


def admin_home(request):
    staff_count = Staff.objects.all().count()
    passenger_count = Passenger.objects.all().count()
    bus_route_count = BusRoute.objects.all().count()
    bus_count = Bus.objects.all().count()
    schedule_count = Schedule.objects.all().count()
    ticket_count = Ticket.objects.all().count()
    payment_count = Payment.objects.all().count()


    return render(request, "bus_ticketing_app/Admin/admin_home_template.html", {
        "staff_count": staff_count,
        "passenger_count": passenger_count,
        "bus_route_count": bus_route_count,
        "bus_count": bus_count,
        "schedule_count": schedule_count,
        "ticket_count": ticket_count,
        "payment_count": payment_count,
    })

def staff(request):
    staffs = Staff.objects.all()
    return render(request, "bus_ticketing_app/Admin/staff.html", {
        "staffs": staffs
    })


def add_staff(request):
    return render(request, "bus_ticketing_app/Admin/add_staff.html")

def add_staff_save(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get("password")
        address = request.POST.get('address')

        try:
            user = CustomUser.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password, user_type=2)
            user.staff.phone_number = phone_number
            user.staff.address = address
            user.save()
            messages.success(request, "Staff Added Successfully!")
            return redirect('bus_ticketing_app:staff')
        except:
            messages.error(request, "Failed to Add Staff!")
            return redirect('bus_ticketing_app:staff')
    else:
        return HttpResponse("Method not allowed")


def passenger(request):
    passengers = Passenger.objects.all()
    return render(request, "bus_ticketing_app/Admin/passenger.html", {
        "passengers": passengers,
    })
    
def add_passenger(request):
    return render(request, "bus_ticketing_app/Admin/add_passenger.html")

    

def add_passenger_save(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get("password")
        address = request.POST.get('address')

        try:
            user = CustomUser.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password, user_type=3)
            user.passenger.phone_number = phone_number
            user.passenger.address = address
            user.save()
            messages.success(request, "Passenger Added Successfully!")
            return redirect('bus_ticketing_app:passenger')
        except:
            messages.error(request, "Failed to Add Passenger!")
            return redirect('bus_ticketing_app:staff')
    else:
        return HttpResponse("Method not allowed")

def bus_route(request):
    bus_routes = BusRoute.objects.all()
    return render(request, "bus_ticketing_app/Admin/bus_route.html", {
        "bus_routes": bus_routes,
    })

def add_bus_route(request):
    return render(request, "bus_ticketing_app/Admin/add_bus_route.html")

def add_bus_route_save(request):
    if request.method == "POST":
        origin = request.POST.get('origin')
        destination = request.POST.get('destination')
        distance = request.POST.get('distance')

        try:
            BusRoute.objects.create(origin=origin, destination=destination, distance=distance)
            messages.success(request, "Route Added Successfully!")
            return redirect('bus_ticketing_app:bus_route')
        except:
            messages.error(request, "Failed to Add Route!")
            return redirect('bus_ticketing_app:staff')
    else:
        return HttpResponse("Method not allowed")
        


def bus(request):
    buses = Bus.objects.all()
    return render(request, "bus_ticketing_app/Admin/bus.html", {
        "buses": buses,
    })


def add_bus(request):
    bus_routes = BusRoute.objects.all()
    return render(request, "bus_ticketing_app/Admin/add_bus.html", {
        "bus_routes": bus_routes,
    })

def add_bus_save(request):
    if request.method == "POST":
        bus_number = request.POST.get('bus_number')
        capacity = request.POST.get('capacity')

        try:
            Bus.objects.create(bus_number=bus_number, capacity=capacity)
            messages.success(request, "Bus Added Successfully!")
            return redirect('bus_ticketing_app:bus')
        except:
            messages.error(request, "Failed to Add Bus!")
            return redirect('bus_ticketing_app:staff')
    else:
        return HttpResponse("Method not allowed")

def edit_staff(request, staff_id):
    staff = Staff.objects.get(admin=staff_id)
    return render(request, "bus_ticketing_app/Admin/edit_staff.html", {
        "staff": staff,
    })

def edit_staff_save(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')

        try:
            user = CustomUser.objects.get(id=staff_id)
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email 
            user.save()

            staff = Staff.objects.get(admin=staff_id)
            staff.address = address
            staff.phone_number = phone_number
            staff.save()

            messages.success(request, "Staff Updated Successfully!")
            return redirect('bus_ticketing_app:staff')
        except:
            messages.error(request, "Failed to Update Staff!")
            return redirect('bus_ticketing_app:staff')
    else:
        return HttpResponse("Method not allowed")

def edit_passenger(request, passenger_id):
    passenger = Passenger.objects.get(admin=passenger_id)
    return render(request, "bus_ticketing_app/Admin/edit_passenger.html", {
        "passenger": passenger,
    })

def edit_passenger_save(request):
    if request.method == 'POST':
        passenger_id = request.POST.get('passenger_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')

        try:
            user = CustomUser.objects.get(id=passenger_id)
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email 
            user.save()

            passenger = Passenger.objects.get(admin=passenger_id)
            passenger.address = address
            passenger.phone_number = phone_number
            passenger.save()

            messages.success(request, "Passenger Updated Successfully!")
            return redirect('bus_ticketing_app:passenger')
        except:
            messages.error(request, "Failed to Update Passenger!")
            return redirect('bus_ticketing_app:staff')
    else:
        return HttpResponse("Method not allowed")
    
def edit_bus_route(request, bus_route_id):
    bus_route = BusRoute.objects.get(id=bus_route_id)
    return render(request, "bus_ticketing_app/Admin/edit_bus_route.html", {
        "bus_route": bus_route,
    })

def edit_bus_route_save(request):
    if request.method == "POST":
        bus_route_id = request.POST.get('bus_route_id')
        origin = request.POST.get('origin')
        destination = request.POST.get('destination')
        distance = request.POST.get('distance')

        try:
            bus_route = BusRoute.objects.get(id=bus_route_id)
            bus_route.origin = origin
            bus_route.destination = destination
            bus_route.distance = distance
            bus_route.save()
            messages.success(request, "Route Updated Successfully!")
            return redirect('bus_ticketing_app:bus_route')
        except:
            messages.error(request, "Failed to Update Route!")
            return redirect('bus_ticketing_app:bus_route')
    else:
        return HttpResponse("Method not allowed")
    
    
def edit_bus(request, bus_id):
    bus = Bus.objects.get(id=bus_id)
    bus_routes = BusRoute.objects.all()
    return render(request, "bus_ticketing_app/Admin/edit_bus.html", {
        "bus": bus,
        "bus_routes": bus_routes,
    })

def edit_bus_save(request):
    if request.method == "POST":
        bus_id = request.POST.get('bus_id')
        bus_number = request.POST.get('bus_number')
        capacity = request.POST.get('capacity')

        try:
            bus = Bus.objects.get(id=bus_id)
            bus.bus_number = bus_number
            bus.capacity = capacity
            bus.save()
            messages.success(request, "Bus Updated Successfully!")
            return redirect('bus_ticketing_app:bus')
        except:
            messages.error(request, "Failed to Update Bus!")
            return redirect('bus_ticketing_app:staff')
    else:
        return HttpResponse("Method not allowed")


def schedule(request):
    schedules = Schedule.objects.all()
    return render(request, "bus_ticketing_app/Admin/schedule.html", {
        "schedules": schedules,
    })

def add_schedule(request):
    bus_routes = BusRoute.objects.all()
    buses = Bus.objects.all()
    return render(request, "bus_ticketing_app/Admin/add_schedule.html", {
        "bus_routes": bus_routes,
        "buses": buses,
    })
    


def add_schedule_save(request):
    if request.method == "POST":
        bus_route_id = request.POST.get('bus_route')
        bus_route = BusRoute.objects.get(id=bus_route_id)
        bus_id = request.POST.get('bus')
        bus = Bus.objects.get(id=bus_id)
        departure_time = request.POST.get('departure_time')
        arrival_time = request.POST.get('arrival_time')

        try:
            Schedule.objects.create(route_id=bus_route, bus_id=bus, departure_time=departure_time, arrival_time=arrival_time)
            messages.success(request, "Schedule Added Successfully!")
            return redirect('bus_ticketing_app:schedule')
        except:
            messages.error(request, "Failed to Add Schedule!")
            return redirect('bus_ticketing_app:schedule')
    else:
        return HttpResponse("Method not allowed")

def edit_schedule(request, schedule_id):
    schedule = Schedule.objects.get(id=schedule_id)
    bus_routes = BusRoute.objects.all()
    buses = Bus.objects.all()
    return render(request, "bus_ticketing_app/Admin/edit_schedule.html", {
        "schedule": schedule,
        "bus_routes": bus_routes,
        "buses": buses,
    })
    

def edit_schedule_save(request):
    if request.method == "POST":
        schedule_id = request.POST.get('schedule_id')
        bus_route_id = request.POST.get('bus_route')
        bus_route = BusRoute.objects.get(id=bus_route_id)
        bus_id = request.POST.get('bus')
        bus = Bus.objects.get(id=bus_id)
        departure_time = request.POST.get('departure_time')
        arrival_time = request.POST.get('arrival_time')

        try:
            schedule = Schedule.objects.get(id=schedule_id)
            schedule.route = bus_route
            schedule.bus = bus
            schedule.departure_time = departure_time
            schedule.arrival_time = arrival_time
            schedule.save()
            messages.success(request, "Schedule Updated Successfully!")
            return redirect('bus_ticketing_app:schedule')
        except:
            messages.error(request, "Failed to Add Schedule!")
            return redirect('bus_ticketing_app:schedule')
    else:
        return HttpResponse("Method not allowed")
    

def delete_schedule(request, schedule_id):
    schedule = Schedule.objects.get(id=schedule_id)
    schedule.delete()
    messages.success(request, "Schedule Deleted")
    return redirect("bus_ticketing_app:schedule")

def delete_staff(request, staff_id):
    staff = Staff.objects.get(admin=staff_id)
    staff.admin.delete()
    messages.success(request, "Staff Deleted")
    return redirect('bus_ticketing_app:staff')

def delete_passenger(request, passenger_id):
    passenger = CustomUser.objects.get(id=passenger_id)
    passenger.delete()
    messages.success(request, "Passenger Deleted")
    return redirect('bus_ticketing_app:passenger')

def delete_bus_route(request, bus_route_id):
    bus_route = BusRoute.objects.get(id=bus_route_id)
    bus_route.delete()
    messages.success(request, "Route Deleted")
    return redirect("bus_ticketing_app:bus_route")

def delete_bus(request, bus_id):
    bus = Bus.objects.get(id=bus_id)
    bus.delete()
    messages.success(request, "Bus Deleted")
    return redirect("bus_ticketing_app:bus")

def payment(request):
    payments = Payment.objects.all()
    return render(request, "bus_ticketing_app/Admin/payment.html", {
        "payments": payments
    })

def add_payment(request):
    passengers = Passenger.objects.all()
    schedules = Schedule.objects.all()
    return render(request, "bus_ticketing_app/Admin/add_payment.html", {
        "passengers": passengers,
        "schedules": schedules,
    })
    

def add_payment_save(request):
    if request.method == "POST":
        passenger_id = request.POST.get('passenger')
        passenger = Passenger.objects.get(admin=passenger_id)
        schedule_id = request.POST.get('schedule')
        schedule = Schedule.objects.get(id=schedule_id)
        amount = request.POST.get('amount')
        payment_status = request.POST.get('payment_status')

        try:
            Payment.objects.create(passenger_id=passenger, schedule_id=schedule, amount=amount, payment_status=payment_status)
            messages.success(request, "Payment Added Successfully!")
            return redirect('bus_ticketing_app:payment')
        except:
            messages.error(request, "Failed to Add Payment!")
            return redirect('bus_ticketing_app:payment')
    else:
        return HttpResponse("Method not allowed")

def edit_payment(request, payment_id):
    passengers = Passenger.objects.all()
    schedules = Schedule.objects.all()
    payment = Payment.objects.get(id=payment_id)
    return render(request, "bus_ticketing_app/Admin/edit_payment.html", {
        "passengers": passengers,
        "schedules": schedules,
        "payment": payment,
    })
    

def edit_payment_save(request):
    if request.method == "POST":
        payment_id = request.POST.get('payment_id')
        passenger_id = request.POST.get('passenger')
        passenger = Passenger.objects.get(admin=passenger_id)
        schedule_id = request.POST.get('schedule')
        schedule = Schedule.objects.get(id=schedule_id)
        amount = request.POST.get('amount')
        payment_status = request.POST.get('payment_status')

        try:
            payment = Payment.objects.get(id=payment_id)
            payment.passenger_id = passenger
            payment.schedule_id = schedule
            payment.amount = amount
            payment.payment_status = payment_status
            payment.save()
            messages.success(request, "Payment Updated Successfully!")
            return redirect('bus_ticketing_app:payment')
        except:
            messages.error(request, "Failed to Update Payment!")
            return redirect('bus_ticketing_app:payment')
    else:
        return HttpResponse("Method not allowed")

def delete_payment(request, payment_id):
    payment = Payment.objects.get(id=payment_id)
    payment.delete()
    messages.success(request, "Payment Deleted")
    return redirect("bus_ticketing_app:payment")


def ticket(request):
    tickets = Ticket.objects.all()
    return render(request, "bus_ticketing_app/Admin/ticket.html", {
        "tickets": tickets,
    })
    

def add_ticket(request):
    passengers = Passenger.objects.all()
    schedules = Schedule.objects.all()
    payments = Payment.objects.all()
    return render(request, "bus_ticketing_app/Admin/add_ticket.html", {
        "passengers": passengers,
        "schedules": schedules,
        "payments": payments,
    })
    
def add_ticket_save(request):
    if request.method == "POST":
        passenger_id = request.POST.get('passenger')
        passenger = Passenger.objects.get(admin=passenger_id)
        schedule_id = request.POST.get('schedule')
        schedule = Schedule.objects.get(id=schedule_id)
        payment_id = request.POST.get('payment')
        payment = Payment.objects.get(id=payment_id)
        seat_number = request.POST.get('seat_number')
        status = request.POST.get('status')

        try:
            Ticket.objects.create(passenger_id=passenger, schedule=schedule, payment=payment, status=status, seat_number=seat_number)
            messages.success(request, "Ticket Added Successfully!")
            return redirect('bus_ticketing_app:ticket')
        except:
            messages.error(request, "Failed to Add Ticket!")
            return redirect('bus_ticketing_app:ticket')
    else:
        return HttpResponse("Method not allowed")

def edit_ticket(request, ticket_id):
    passengers = Passenger.objects.all()
    schedules = Schedule.objects.all()
    payments = Payment.objects.all()
    ticket = Ticket.objects.get(id=ticket_id)
    return render(request, "bus_ticketing_app/Admin/edit_ticket.html", {
        "passengers": passengers,
        "schedules": schedules,
        "payments": payments,
        "ticket": ticket,
    })
    

def edit_ticket_save(request):
    if request.method == "POST":
        ticket_id = request.POST.get('ticket_id')
        passenger_id = request.POST.get('passenger')
        passenger = Passenger.objects.get(admin=passenger_id)
        schedule_id = request.POST.get('schedule')
        schedule = Schedule.objects.get(id=schedule_id)
        payment_id = request.POST.get('payment')
        payment = Payment.objects.get(id=payment_id)
        seat_number = request.POST.get('seat_number')
        status = request.POST.get('status')

        # try:
        ticket = Ticket.objects.get(id=ticket_id)
        ticket.passenger_id = passenger
        ticket.schedule = schedule
        ticket.payment_id = payment
        ticket.seat_number = seat_number
        ticket.status = status
        ticket.save()
        messages.success(request, "Ticket Updated Successfully!")
        return redirect('bus_ticketing_app:ticket')
        # except:
        #     messages.error(request, "Failed to Update Ticket!")
        #     return redirect('bus_ticketing_app:ticket')
    else:
        return redirect('bus_ticketing_app:ticket')

def delete_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    ticket.delete()
    messages.error(request, "Ticket Deleted")
    return redirect("bus_ticketing_app:ticket")

def admin_profile(request):
    return render(request, "bus_ticketing_app/Admin/admin_profile.html", {
    })
    

def admin_profile_save(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        user = CustomUser.objects.get(id=request.user.id)
        user.first_name = first_name
        user.last_name = last_name
        if password != None or password != "":
            user.set_password(password)
        user.save()
        return redirect("bus_ticketing_app:admin_home")
    else:
        return redirect("bus_ticketing_app:admin_home")
