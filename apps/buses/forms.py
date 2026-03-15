from django import forms
from .models import Bus

class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ['plate_number', 'capacity', 'bus_type', 'is_active']
        widgets = {
            'plate_number': forms.TextInput(attrs={'class': 'form-input'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-input'}),
            'bus_type': forms.Select(attrs={'class': 'form-input'}),
        }
