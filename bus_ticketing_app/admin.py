from django.contrib import admin

# Register your models here.
from .models import Passenger, BusCompanyStaff, Admin, Bus, BusRoute, Ticket

admin.site.register(Passenger)
admin.site.register(BusCompanyStaff)
admin.site.register(Admin)
admin.site.register(Bus)
admin.site.register(BusRoute)
admin.site.register(Ticket)
