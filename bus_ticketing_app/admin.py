from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Passenger, BusCompanyStaff, BusRoute, Bus, Book, Ticket, Driver

# Register your models here.
class CustomUserAdmin(UserAdmin):
    pass

# Register the custom models with the admin site
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Passenger)
admin.site.register(BusCompanyStaff)
admin.site.register(BusRoute)
admin.site.register(Bus)
admin.site.register(Book)
admin.site.register(Ticket)
admin.site.register(Driver)
