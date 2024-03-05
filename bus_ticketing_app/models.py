from django.db import models

# Create your models here.
class Passenger(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class BusCompanyStaff(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    position = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Admin(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Bus(models.Model):
    company = models.ForeignKey(BusCompanyStaff, on_delete=models.CASCADE)
    route = models.ForeignKey('BusRoute', on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()

    def __str__(self):
        return f"{self.company.name} - {self.route.origin} to {self.route.destination}"

    class Meta:
        verbose_name_plural = 'buses'


class BusRoute(models.Model):
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    distance = models.FloatField()
    duration = models.DurationField()

    def __str__(self):
        return f"{self.origin} to {self.destination}"

class Ticket(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.passenger.name} - {self.bus.company.name} - {self.departure_t}"