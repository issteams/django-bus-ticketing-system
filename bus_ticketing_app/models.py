from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    # Add custom fields as needed
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Custom User'
    
    def __str__(self):
        return self.username

class Passenger(models.Model):
    user = models.OneToOneField(CustomUser, null=True, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Passenger'
    
    def __str__(self):
        return self.user.username

class BusCompanyStaff(models.Model):
    user = models.OneToOneField(CustomUser, null=True, on_delete=models.CASCADE)
    position = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Bus Company Staff'

    def __str__(self):
        return self.user.username

class BusRoute(models.Model):
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    date = models.DateField(null=True)
    departure_time = models.DateTimeField(null=True)
    arrival_time = models.DateTimeField(null=True)
    total_seats = models.IntegerField(null=True)
    available_seats = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.origin} to {self.destination}"

class Bus(models.Model):
    company = models.ForeignKey(BusCompanyStaff, on_delete=models.CASCADE)
    route = models.ForeignKey(BusRoute, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()

    def __str__(self):
        return f"{self.company.user.username} - {self.route.origin} to {self.route.destination}"

    class Meta:
        verbose_name_plural = 'Buses'

class Book(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    bus_route = models.ForeignKey(BusRoute, on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    date_booked = models.DateTimeField(auto_now_add=True)

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    departure_time = models.DateTimeField(auto_now_add=True)
    arrival_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.passenger.user.username} - {self.bus.company.user.username} - {self.departure_time}"

class Driver(models.Model):
    user = models.OneToOneField(CustomUser, null=True, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Driver'

    def __str__(self):
        return self.user.username
