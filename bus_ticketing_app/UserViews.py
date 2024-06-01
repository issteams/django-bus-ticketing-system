from django.shortcuts import render, redirect, get_object_or_404
from .models import BusRoute, Schedule, Ticket, Payment, Passenger
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from datetime import datetime
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
import requests
import json


@login_required
def user_home(request):
    user = request.user
    upcoming_bookings = Ticket.objects.filter(passenger__admin=user, schedule__departure_time__gte=timezone.now()).order_by('schedule__departure_time')

    context = {
        'user': user,
        'upcoming_bookings': upcoming_bookings,
    }
    return render(request, "bus_ticketing_app/users/user_home.html", context)


@login_required
def search_result(request):
    if request.method == "GET":
        origin = request.GET.get('origin')
        destination = request.GET.get('destination')
        date = request.GET.get('date')

        if origin and destination and date:
            # Parse the date string into a datetime object
            try:
                travel_date = datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                return render(request, "bus_ticketing_app/users/search_result.html", {
                    "message": "Invalid date format. Please use YYYY-MM-DD."
                })

            # Find routes that match the origin and destination
            routes = BusRoute.objects.filter(Q(origin__iexact=origin) & Q(destination__iexact=destination))

            # Find schedules that match the routes and the given date
            schedules = Schedule.objects.filter(route_id__in=routes, departure_time__date=travel_date)

            if schedules.exists():
                return render(request, "bus_ticketing_app/users/search_result.html", {
                    "schedules": schedules,
                    "date": date,
                })
            else:
                return render(request, "bus_ticketing_app/users/search_result.html", {
                    "message": "No Result",
                })
        else:
            return render(request, "bus_ticketing_app/users/search_result.html", {
                "message": "Please provide origin, destination, and date."
            })
    else:
        return render(request, "bus_ticketing_app/users/search_result.html", {
            "message": "Invalid request method."
        })

def book_seat(request, schedule_id):
    schedule = Schedule.objects.get(id=schedule_id)
    seats = []
    schedule_id = schedule.id
    capacity = schedule.bus_id.capacity
    for seat in range(1, capacity + 1):
        seats.append(seat)
    return render(request, "bus_ticketing_app/users/book_seat.html", {
        "schedule_id": schedule_id,
        "seats": seats,
    })
       
@login_required
def get_book_seat(request, schedule_id):
    if request.method == 'POST':
        seat_number = request.POST.get('seat_number')
        user = request.user.id
        try:
            passenger = Passenger.objects.get(admin=user)
        except Student.DoesNotExist:
            # Handle the case where the student doesn't exist
            messages.error(request, "Passenger not found")
            return redirect("book_seat", schedule_id)

        try:
            schedule = Schedule.objects.get(id=schedule_id)
            schedule.seat_number = seat_number
            schedule.save()
        except Schedule.DoesNotExist:
            # Handle the case where the schedule doesn't exist
            return HttpResponse("Schedule not found")

        # Check if the seat is already booked
        if Ticket.objects.filter(schedule=schedule, seat_number=seat_number).exists():
            messages.error(request, "Seat already booked")
            return redirect("bus_ticketing_app:book_seat", schedule_id)

        # Create a new ticket for the student
        ticket = Ticket.objects.create(passenger=passenger, schedule=schedule, seat_number=seat_number, status="pending")
        messages.success(request, "Seat booked successfully")
        return redirect("bus_ticketing_app:make_payment", schedule_id)

    else:
        # Handle GET request if needed
        pass

@login_required
def make_payment(request, schedule_id):
    if request.method == 'POST':
        seat_number = request.POST.get('seat_number')
        amount = request.POST.get('amount')
        user = request.user

        try:
            schedule = Schedule.objects.get(id=schedule_id)
            schedule.seat_number = seat_number
            schedule.save()
            student = Student.objects.get(admin=user)

            if Ticket.objects.filter(schedule=schedule, seat_number=seat_number).exists():
                messages.error(request, "Seat Already Booked")
                return redirect('book_seat', schedule_id)

            # Generate a unique reference for the payment
            reference = f"{user.id}-{schedule_id}-{seat_number}-{int(datetime.now().timestamp())}"

            # Create a pending ticket
            ticket = Ticket.objects.create(
                student=student,
                schedule=schedule,
                seat_number=seat_number,
                status="pending",
                payment_reference=reference
            )

            # Create a Paystack payment session
            headers = {
                'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
                'Content-Type': 'application/json'
            }
            data = {
                'email': user.email,
                'amount': int(amount) * 100,  # Amount in kobo
                'reference': reference,
                'callback_url': request.build_absolute_uri('/verify_payment/')
            }

            response = requests.post('https://api.paystack.co/transaction/initialize', headers=headers, json=data)
            response_data = response.json()

            if response_data['status']:
                payment_url = response_data['data']['authorization_url']
                return redirect(payment_url)
            else:
                messages.error(request, f"Payment initialization failed: {response_data['message']}")
                return redirect('make_payment', schedule_id)

        except Schedule.DoesNotExist:
            return HttpResponse("Schedule Not Found")
        except Student.DoesNotExist:
            return HttpResponse("Student Not Found")
    else:
        schedule = get_object_or_404(Schedule, id=schedule_id)
        amount = 1000  # Placeholder amount; replace with actual amount calculation

        return render(request, "bus_ticketing_app/users/payment.html", {
            "schedule": schedule,
            "amount": amount,
            "seat_number": schedule.seat_number,
            "paystack_public_key": settings.PAYSTACK_PUBLIC_KEY
        })

@csrf_exempt
def verify_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        reference = data.get('reference')
        schedule_id = data.get('schedule_id')
        seat_number = data.get('seat_number')

        url = f"https://api.paystack.co/transaction/verify/{reference}"
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
        }
        response = requests.get(url, headers=headers)
        response_data = response.json()

        if response_data['status'] and response_data['data']['status'] == 'success':
            # Payment was successful
            amount = response_data['data']['amount'] / 100  # Convert from kobo to naira

            try:
                schedule = Schedule.objects.get(id=schedule_id)
                user = request.user
                passenger = Passenger.objects.get(admin=user)

                # Create or get the Ticket
                ticket, created = Ticket.objects.get_or_create(
                    schedule=schedule,
                    seat_number=seat_number,
                    defaults={'passenger': passenger, 'status': 'pending', 'payment_reference': reference}
                )

                # Ensure the payment is only recorded once
                if ticket.status != "confirmed":
                    # Create Payment record
                    payment = Payment.objects.create(
                        passenger_id=passenger,
                        schedule_id=schedule,
                        amount=amount,
                        payment_status='Paid'
                    )

                    # Update Ticket record
                    ticket.status = "confirmed"
                    ticket.payment = payment
                    ticket.payment_reference = reference
                    ticket.save()

                    return JsonResponse({'status': 'success'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Ticket already confirmed'}, status=400)

            except (Schedule.DoesNotExist, Passenger.DoesNotExist) as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        else:
            return JsonResponse({'status': 'error', 'message': 'Payment verification failed'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)



@login_required
def payment_success(request):
    messages.success(request, "Payment successful! Your seat has been booked.")
    return render(request, "bus_ticketing_app/users/payment_success.html")

@login_required
def payment_cancel(request):
    pass


def user_books(request):
    pass

def user_tickets(request):
    passenger = Passenger.objects.get(admin=request.user.id)
    tickets = Ticket.objects.filter(passenger=passenger)
    return render(request, "bus_ticketing_app/users/user_tickets.html", {
        "tickets": tickets,
    })

def user_payments(request):
    passenger = Passenger.objects.get(admin=request.user.id)
    payments = Payment.objects.filter(passenger_id=passenger)
    return render(request, "bus_ticketing_app/users/user_payments.html", {
        "payments": payments,
    })
    

@login_required
def print_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, passenger__admin=request.user)
    template = get_template('bus_ticketing_app/users/print_ticket.html')
    context = {
        'ticket': ticket,
    }
    html = template.render(context)
    return HttpResponse(html)



    
        

