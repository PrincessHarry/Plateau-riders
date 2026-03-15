import json
import hashlib
import hmac
from datetime import datetime, date
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Trip, Booking
from .forms import TripSearchForm, PassengerDetailsForm, TripForm
from apps.routes.models import Route, RouteStop
from apps.buses.models import Bus, Seat
from django.conf import settings


def home(request):
    form = TripSearchForm()
    featured_routes = Route.objects.filter(is_active=True)[:6]
    upcoming_trips = Trip.objects.filter(
        status='scheduled',
        departure_time__gte=timezone.now()
    ).select_related('route', 'bus')[:5]
    return render(request, 'booking/home.html', {
        'form': form,
        'featured_routes': featured_routes,
        'upcoming_trips': upcoming_trips,
    })


def search_trips(request):
    form = TripSearchForm(request.GET or None)
    results = []
    origin = request.GET.get('origin', '').strip()
    destination = request.GET.get('destination', '').strip()
    travel_date = request.GET.get('travel_date', '')

    if origin and destination and travel_date:
        try:
            search_date = datetime.strptime(travel_date, '%Y-%m-%d').date()
        except ValueError:
            search_date = date.today()

        # Smart route matching: find trips where origin matches
        # and destination is either the final destination or an intermediate stop
        matched_trips = []
        all_trips = Trip.objects.filter(
            status__in=['scheduled', 'boarding'],
            departure_time__date=search_date
        ).select_related('route', 'bus', 'route').prefetch_related('route__stops', 'bus__seats')

        for trip in all_trips:
            route = trip.route
            all_stops = route.get_all_stops()

            # Find origin position
            origin_idx = None
            for i, stop in enumerate(all_stops):
                if stop.lower() == origin.lower():
                    origin_idx = i
                    break

            # Find destination position
            dest_idx = None
            for i, stop in enumerate(all_stops):
                if stop.lower() == destination.lower():
                    dest_idx = i
                    break

            # Valid booking: origin appears BEFORE destination
            if origin_idx is not None and dest_idx is not None and origin_idx < dest_idx:
                # Calculate price for this segment
                price = _calculate_segment_price(route, origin_idx, dest_idx, trip.price)
                matched_trips.append({
                    'trip': trip,
                    'origin': origin,
                    'destination': destination,
                    'drop_point': destination,
                    'segment_price': price,
                    'available_seats': trip.available_seat_count(),
                })

        results = matched_trips

    return render(request, 'booking/search_results.html', {
        'form': form,
        'results': results,
        'origin': origin,
        'destination': destination,
        'travel_date': travel_date,
    })


def _calculate_segment_price(route, origin_idx, dest_idx, base_price):
    """Calculate proportional price for a route segment"""
    all_stops = route.get_all_stops()
    total_stops = len(all_stops) - 1
    if total_stops == 0:
        return base_price
    segment_length = dest_idx - origin_idx
    ratio = segment_length / total_stops
    return round(float(base_price) * ratio, 2)


def select_seats(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)
    origin = request.GET.get('origin', trip.route.origin)
    destination = request.GET.get('destination', trip.route.destination)
    price = request.GET.get('price', trip.price)

    seats = trip.bus.seats.all().order_by('seat_number')
    booked_seat_ids = trip.booked_seat_ids()

    seat_data = []
    for seat in seats:
        seat_data.append({
            'id': seat.id,
            'number': seat.seat_number,
            'is_booked': seat.id in booked_seat_ids,
        })

    form = PassengerDetailsForm()

    return render(request, 'booking/select_seats.html', {
        'trip': trip,
        'seats': seats,
        'seat_data': json.dumps(seat_data),
        'booked_seat_ids': booked_seat_ids,
        'origin': origin,
        'destination': destination,
        'price': price,
        'form': form,
        'bus': trip.bus,
    })


def confirm_booking(request, trip_id):
    if request.method != 'POST':
        return redirect('home')

    trip = get_object_or_404(Trip, pk=trip_id)
    seat_id = request.POST.get('seat_id')
    origin = request.POST.get('origin', trip.route.origin)
    destination = request.POST.get('destination', trip.route.destination)
    price = request.POST.get('price', trip.price)

    seat = get_object_or_404(Seat, pk=seat_id, bus=trip.bus)

    # Check if seat is still available
    if seat.id in trip.booked_seat_ids():
        messages.error(request, 'This seat was just booked. Please select another seat.')
        return redirect('select_seats', trip_id=trip_id)

    form = PassengerDetailsForm(request.POST, request.FILES)
    if not form.is_valid():
        messages.error(request, 'Please fill in all required fields correctly.')
        return redirect('select_seats', trip_id=trip_id)

    booking = form.save(commit=False)
    booking.trip = trip
    booking.seat = seat
    booking.start_stop = origin
    booking.end_stop = destination
    booking.amount_paid = price
    booking.status = 'pending'
    if request.user.is_authenticated:
        booking.passenger = request.user
    booking.save()

    return redirect('booking_payment', booking_ref=booking.booking_reference)


def booking_payment(request, booking_ref):
    booking = get_object_or_404(Booking, booking_reference=booking_ref)
    return render(request, 'booking/payment.html', {
        'booking': booking,
        'monnify_api_key': settings.MONNIFY_API_KEY,
        'monnify_contract_code': settings.MONNIFY_CONTRACT_CODE,
    })


@csrf_exempt
def verify_payment(request):
    """Called after Monnify payment completion"""
    if request.method == 'POST':
        data = json.loads(request.body)
        booking_ref = data.get('booking_reference')
        payment_ref = data.get('transactionReference', '')

        try:
            booking = Booking.objects.get(booking_reference=booking_ref)
            booking.status = 'confirmed'
            booking.payment_reference = payment_ref
            booking.save()
            return JsonResponse({'success': True, 'redirect': f'/booking/ticket/{booking_ref}/'})
        except Booking.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Booking not found'})

    return JsonResponse({'success': False})


def booking_ticket(request, booking_ref):
    booking = get_object_or_404(Booking, booking_reference=booking_ref)
    return render(request, 'booking/ticket.html', {'booking': booking})


def booking_detail(request, booking_ref):
    booking = get_object_or_404(Booking, booking_reference=booking_ref)
    return render(request, 'booking/booking_detail.html', {'booking': booking})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(passenger=request.user).order_by('-created_at')
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})


# Staff/Admin Views
@login_required
def trip_list(request):
    trips = Trip.objects.select_related('route', 'bus').order_by('-departure_time')
    return render(request, 'booking/trip_list.html', {'trips': trips})


@login_required
def trip_create(request):
    form = TripForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Trip scheduled successfully.')
        return redirect('trip_list')
    return render(request, 'booking/trip_form.html', {'form': form, 'title': 'Schedule New Trip'})


@login_required
def trip_edit(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    form = TripForm(request.POST or None, instance=trip)
    if form.is_valid():
        form.save()
        messages.success(request, 'Trip updated successfully.')
        return redirect('trip_list')
    return render(request, 'booking/trip_form.html', {'form': form, 'title': 'Edit Trip', 'trip': trip})


def get_seat_availability(request, trip_id):
    """API endpoint for seat availability"""
    trip = get_object_or_404(Trip, pk=trip_id)
    booked = trip.booked_seat_ids()
    return JsonResponse({'booked_seats': booked})
