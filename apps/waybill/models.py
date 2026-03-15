import random
import string
from django.db import models
from apps.booking.models import Trip

class Waybill(models.Model):
    STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('loaded', 'Loaded'),
        ('in_transit', 'In Transit'),
        ('arrived', 'Arrived'),
        ('collected', 'Collected'),
    ]
    sender_name = models.CharField(max_length=200)
    sender_phone = models.CharField(max_length=15)
    receiver_name = models.CharField(max_length=200)
    receiver_phone = models.CharField(max_length=15)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    description = models.TextField()
    weight = models.DecimalField(max_digits=6, decimal_places=2, help_text='Weight in kg')
    tracking_code = models.CharField(max_length=20, unique=True, blank=True)
    trip = models.ForeignKey(Trip, on_delete=models.SET_NULL, null=True, blank=True, related_name='waybills')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='booked')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_reference = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.tracking_code:
            self.tracking_code = self._generate_tracking()
        super().save(*args, **kwargs)

    def _generate_tracking(self):
        prefix = 'WB'
        suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        return f"{prefix}{suffix}"

    def __str__(self):
        return f"{self.tracking_code} - {self.sender_name} → {self.receiver_name}"

    def calculate_amount(self):
        base = 500
        per_kg = 200
        return base + (float(self.weight) * per_kg)


class WaybillStatusHistory(models.Model):
    waybill = models.ForeignKey(Waybill, on_delete=models.CASCADE, related_name='status_history')
    status = models.CharField(max_length=20, choices=Waybill.STATUS_CHOICES)
    note = models.TextField(blank=True)
    updated_by = models.CharField(max_length=100, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.waybill.tracking_code} - {self.status} at {self.updated_at}"
