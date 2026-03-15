from django import forms
from django.forms import inlineformset_factory
from .models import Route, RouteStop

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['origin', 'destination', 'base_price', 'is_active']
        widgets = {
            'origin': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Jos'}),
            'destination': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Lagos'}),
            'base_price': forms.NumberInput(attrs={'class': 'form-input'}),
        }

RouteStopFormSet = inlineformset_factory(
    Route, RouteStop,
    fields=['location', 'order', 'price_from_origin'],
    extra=5,
    can_delete=True,
    widgets={
        'location': forms.TextInput(attrs={'class': 'form-input'}),
        'order': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
        'price_from_origin': forms.NumberInput(attrs={'class': 'form-input'}),
    }
)
