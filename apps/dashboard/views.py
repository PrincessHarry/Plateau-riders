from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import date, timedelta
from apps.booking.models import Trip, Booking
from apps.waybill.models import Waybill
from apps.buses.models import Bus
from apps.routes.models import Route

@login_required
def dashboard(request):
    if not request.user.is_staff_member:
        return redirect('home')

    today = date.today()
    this_month_start = today.replace(day=1)

    # Stats
    total_trips = Trip.objects.count()
    bookings_today = Booking.objects.filter(created_at__date=today).count()
    waybills_today = Waybill.objects.filter(created_at__date=today).count()
    total_buses = Bus.objects.filter(is_active=True).count()
    total_routes = Route.objects.filter(is_active=True).count()

    # Revenue
    monthly_revenue = Booking.objects.filter(
        created_at__date__gte=this_month_start,
        status='confirmed'
    ).aggregate(total=Sum('amount_paid'))['total'] or 0

    waybill_revenue = Waybill.objects.filter(
        created_at__date__gte=this_month_start
    ).aggregate(total=Sum('amount'))['total'] or 0

    total_revenue = float(monthly_revenue) + float(waybill_revenue)

    # Recent bookings
    recent_bookings = Booking.objects.select_related('trip__route', 'seat').order_by('-created_at')[:10]

    # Recent waybills
    recent_waybills = Waybill.objects.order_by('-created_at')[:10]

    # Upcoming trips
    upcoming_trips = Trip.objects.filter(
        departure_time__gte=timezone.now(),
        status__in=['scheduled', 'boarding']
    ).select_related('route', 'bus').order_by('departure_time')[:8]

    # Active waybills by status
    waybill_stats = {}
    for status, label in Waybill.STATUS_CHOICES:
        waybill_stats[status] = {'label': label, 'count': Waybill.objects.filter(status=status).count()}

    return render(request, 'dashboard/dashboard.html', {
        'total_trips': total_trips,
        'bookings_today': bookings_today,
        'waybills_today': waybills_today,
        'total_buses': total_buses,
        'total_routes': total_routes,
        'total_revenue': total_revenue,
        'monthly_revenue': monthly_revenue,
        'waybill_revenue': waybill_revenue,
        'recent_bookings': recent_bookings,
        'recent_waybills': recent_waybills,
        'upcoming_trips': upcoming_trips,
        'waybill_stats': waybill_stats,
        'today': today,
    })
