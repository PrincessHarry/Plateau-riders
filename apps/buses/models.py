from django.db import models

class Bus(models.Model):
    BUS_TYPES = [
        ('standard', 'Standard Bus'),
        ('luxury', 'Luxury Bus'),
        ('minibus', 'Minibus'),
        ('coaster', 'Coaster'),
    ]
    plate_number = models.CharField(max_length=20, unique=True)
    capacity = models.PositiveIntegerField()
    bus_type = models.CharField(max_length=20, choices=BUS_TYPES, default='standard')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.plate_number} ({self.bus_type} - {self.capacity} seats)"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            for i in range(1, self.capacity + 1):
                Seat.objects.get_or_create(bus=self, seat_number=i)

class Seat(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.PositiveIntegerField()

    class Meta:
        unique_together = ('bus', 'seat_number')
        ordering = ['seat_number']

    def __str__(self):
        return f"Seat {self.seat_number} - {self.bus.plate_number}"
