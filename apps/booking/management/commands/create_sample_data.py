"""
Management command to populate sample data for Plateau Riders.
Run: python manage.py create_sample_data
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.buses.models import Bus
from apps.routes.models import Route, RouteStop
from apps.booking.models import Trip
from apps.accounts.models import User


class Command(BaseCommand):
    help = 'Create sample data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Buses
        bus1, _ = Bus.objects.get_or_create(
            plate_number='JOS-001-AA',
            defaults={'capacity': 18, 'bus_type': 'luxury', 'is_active': True}
        )
        bus2, _ = Bus.objects.get_or_create(
            plate_number='JOS-002-BB',
            defaults={'capacity': 14, 'bus_type': 'standard', 'is_active': True}
        )
        self.stdout.write(f'  ✓ Buses created')

        # Jos → Lagos Route
        route1, _ = Route.objects.get_or_create(
            origin='Jos', destination='Lagos',
            defaults={'base_price': 15000, 'is_active': True}
        )
        stops1 = [
            ('Abuja', 1, 3000),
            ('Lokoja', 2, 6000),
            ('Ilorin', 3, 10000),
            ('Ibadan', 4, 13000),
        ]
        for loc, order, price in stops1:
            RouteStop.objects.get_or_create(
                route=route1, order=order,
                defaults={'location': loc, 'price_from_origin': price}
            )

        # Jos → Abuja Route
        route2, _ = Route.objects.get_or_create(
            origin='Jos', destination='Abuja',
            defaults={'base_price': 3000, 'is_active': True}
        )

        # Abuja → Lagos
        route3, _ = Route.objects.get_or_create(
            origin='Abuja', destination='Lagos',
            defaults={'base_price': 12000, 'is_active': True}
        )
        RouteStop.objects.get_or_create(route=route3, order=1, defaults={'location': 'Lokoja', 'price_from_origin': 4000})
        RouteStop.objects.get_or_create(route=route3, order=2, defaults={'location': 'Ibadan', 'price_from_origin': 9000})

        self.stdout.write(f'  ✓ Routes created')

        # Trips
        now = timezone.now()
        trips_data = [
            (route1, bus1, now + timedelta(hours=2), 15000),
            (route1, bus2, now + timedelta(days=1, hours=6), 15000),
            (route2, bus1, now + timedelta(days=1, hours=8), 3000),
            (route3, bus2, now + timedelta(hours=5), 12000),
        ]
        for route, bus, dep, price in trips_data:
            Trip.objects.get_or_create(
                route=route, bus=bus, departure_time=dep,
                defaults={'price': price, 'status': 'scheduled'}
            )
        self.stdout.write(f'  ✓ Trips scheduled')

        # Staff user
        if not User.objects.filter(username='staff').exists():
            User.objects.create_user(
                username='staff',
                password='staff123',
                email='staff@plateauriders.com',
                role='staff'
            )
            self.stdout.write(f'  ✓ Staff user created (username: staff, password: staff123)')

        self.stdout.write(self.style.SUCCESS('\n✅ Sample data created successfully!'))
        self.stdout.write('  Run: python manage.py runserver')
        self.stdout.write('  Visit: http://localhost:8000/')
