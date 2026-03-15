from django.db import models

class Route(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.origin} → {self.destination}"

    def get_stops_ordered(self):
        return self.stops.order_by('order')

    def get_all_stops(self):
        """Returns all locations including origin and destination as ordered list"""
        stops = list(self.stops.order_by('order').values_list('location', flat=True))
        return [self.origin] + stops + [self.destination]

class RouteStop(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='stops')
    location = models.CharField(max_length=100)
    order = models.PositiveIntegerField()
    price_from_origin = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ['order']
        unique_together = ('route', 'order')

    def __str__(self):
        return f"{self.route} - Stop {self.order}: {self.location}"
