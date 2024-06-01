from django.shortcuts import render


def staff_home(request):
    return render(request, "bus_ticketing_app/staff/staff_home.html", {})
    