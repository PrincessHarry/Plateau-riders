import uuid
import random
import string
from django.db import models
from apps.accounts.models import User
from apps.routes.models import Route, RouteStop
from apps.buses.models import Bus, Seat

class Trip(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('boarding', 'Boarding'),
        ('in_transit', 'In Transit'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='trips')
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='trips')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.route} - {self.departure_time.strftime('%d %b %Y %H:%M')}"

    def available_seats(self):
        booked = self.bookings.filter(
            status__in=['confirmed', 'pending']
        ).values_list('seat_id', flat=True)
        return self.bus.seats.exclude(id__in=booked)

    def booked_seat_ids(self):
        return list(self.bookings.filter(
            status__in=['confirmed', 'pending']
        ).values_list('seat_id', flat=True))

    def available_seat_count(self):
        return self.available_seats().count()


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='bookings')
    passenger = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    start_stop = models.CharField(max_length=100)
    end_stop = models.CharField(max_length=100)
    seat = models.ForeignKey(Seat, on_delete=models.SET_NULL, null=True, related_name='bookings')
    passenger_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    passenger_photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    booking_reference = models.CharField(max_length=20, unique=True, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_reference = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.booking_reference:
            self.booking_reference = self._generate_reference()
        super().save(*args, **kwargs)

    def _generate_reference(self):
        prefix = 'PR'
        suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        return f"{prefix}{suffix}"

    def __str__(self):
        return f"{self.booking_reference} - {self.passenger_name}"
