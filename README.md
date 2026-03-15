# Plateau Riders — Transport Booking & Waybill System

A full-stack Django transport booking platform with seat selection, waybill management, parcel tracking, and Monnify payment integration.

## Features

- 🚌 **Trip Booking** — Search routes, pick seats visually, upload passenger photo
- 🗺️ **Smart Route Matching** — Book intermediate stops (Jos → Ibadan on a Jos → Lagos bus)
- 💺 **Visual Seat Map** — Green/Black/Yellow seat status, real-time selection
- 📷 **Photo Tickets** — Passenger photo printed on ticket with QR code
- 📦 **Waybill System** — Create parcels, auto-generate tracking code
- 📍 **Parcel Tracking** — Real-time status timeline (Booked → Collected)
- 💳 **Monnify Payment** — Cards, bank transfer, USSD
- 📊 **Admin Dashboard** — Revenue, trips, bookings, waybill stats
- 📱 **Mobile Responsive** — Works on all screen sizes

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Apply migrations
python manage.py makemigrations accounts buses routes booking waybill
python manage.py migrate

# 3. Create superuser
python manage.py createsuperuser

# 4. (Optional) Load sample data
python manage.py loaddata sample_data.json

# 5. Run development server
python manage.py runserver
```

## User Roles

| Role | Access |
|------|--------|
| passenger | Book trips, send parcels, track parcels |
| staff | + Manage waybill status, view dashboard |
| admin | + Full access to all management features |

After creating superuser, visit `/admin/` to set user roles.

## Setting Staff/Admin Roles

1. Go to `http://localhost:8000/admin/`
2. Log in as superuser
3. Go to Users → select user → change Role field

Or via Django shell:
```python
python manage.py shell
from apps.accounts.models import User
u = User.objects.get(username='yourusername')
u.role = 'admin'  # or 'staff'
u.save()
```

## Monnify Integration

1. Sign up at https://monnify.com
2. Get your API Key, Secret Key, and Contract Code
3. Update `plateau_riders/settings.py`:

```python
MONNIFY_API_KEY = 'your-api-key'
MONNIFY_SECRET_KEY = 'your-secret-key'
MONNIFY_CONTRACT_CODE = 'your-contract-code'
MONNIFY_BASE_URL = 'https://api.monnify.com'  # Live URL
```

For sandbox testing, keep the sandbox URL.

## Sample Data Setup

After running migrations, add data via the admin panel or API:

1. **Add a Bus**: `/admin/buses/bus/add/` — seats auto-created
2. **Add a Route**: `/admin/routes/route/add/`
3. **Add Route Stops**: `/admin/routes/routestop/add/`
4. **Schedule a Trip**: `/admin/booking/trip/add/`

Or via the web UI (requires staff/admin login):
- `/buses/create/` — Add bus
- `/routes/create/` — Add route
- `/trips/create/` — Schedule trip

## URL Structure

| URL | Description |
|-----|-------------|
| `/` | Homepage with search |
| `/search/` | Search results |
| `/booking/seats/<id>/` | Seat selection |
| `/booking/ticket/<ref>/` | View/print ticket |
| `/waybill/send/` | Create waybill |
| `/waybill/track/` | Track parcel |
| `/dashboard/` | Staff dashboard |
| `/trips/` | Trip management |
| `/buses/` | Bus management |
| `/routes/` | Route management |
| `/admin/` | Django admin |

## Tech Stack

- **Backend**: Django 4.2, Django REST Framework
- **Frontend**: TailwindCSS (CDN), Vanilla JS
- **Database**: SQLite (dev), PostgreSQL (prod)
- **Auth**: Django's built-in auth + custom User model
- **Payments**: Monnify SDK
- **Media**: Pillow for photo uploads

## Smart Route Matching Logic

Route: Jos → Abuja → Lokoja → Ilorin → Ibadan → Lagos

Allowed bookings:
- ✅ Jos → Abuja
- ✅ Jos → Lokoja
- ✅ Jos → Lagos
- ✅ Abuja → Lokoja
- ✅ Lokoja → Lagos

Blocked:
- ❌ Ibadan → Abuja (wrong direction)
- ❌ Lagos → Jos (no backward travel)

The system checks that the origin index appears BEFORE the destination index in the stop order.

## Branding

Primary colors defined in `base.html`:
- Primary Green: `#1E7F3B`
- Dark Green: `#145A2A`
- Black: `#000000`

Customize in the Tailwind config block inside `templates/base.html`.
