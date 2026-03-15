from django import forms
from .models import Trip, Booking
from apps.routes.models import Route

class TripSearchForm(forms.Form):
    origin = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-input w-full px-4 py-3 rounded-lg border border-gray-300',
            'placeholder': 'From (e.g. Jos)',
            'list': 'cities-list'
        })
    )
    destination = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-input w-full px-4 py-3 rounded-lg border border-gray-300',
            'placeholder': 'To (e.g. Lagos)',
            'list': 'cities-list'
        })
    )
    travel_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-input w-full px-4 py-3 rounded-lg border border-gray-300',
            'type': 'date'
        })
    )

class PassengerDetailsForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['passenger_name', 'phone', 'passenger_photo']
        widgets = {
            'passenger_name': forms.TextInput(attrs={
                'class': 'form-input w-full px-4 py-3 rounded-lg border border-gray-300',
                'placeholder': 'Full name as on ID'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input w-full px-4 py-3 rounded-lg border border-gray-300',
                'placeholder': '08012345678'
            }),
            'passenger_photo': forms.FileInput(attrs={
                'class': 'form-input w-full px-4 py-3 rounded-lg border border-gray-300',
                'accept': 'image/*',
                'capture': 'user'
            }),
        }

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['route', 'bus', 'departure_time', 'arrival_time', 'price', 'status']
        widgets = {
            'departure_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-input'}),
            'arrival_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-input'}),
            'route': forms.Select(attrs={'class': 'form-input'}),
            'bus': forms.Select(attrs={'class': 'form-input'}),
            'price': forms.NumberInput(attrs={'class': 'form-input'}),
            'status': forms.Select(attrs={'class': 'form-input'}),
        }
