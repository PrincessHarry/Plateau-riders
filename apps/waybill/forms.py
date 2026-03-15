from django import forms
from .models import Waybill, WaybillStatusHistory
from apps.booking.models import Trip

INPUT_CLASS = 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-green-600'

class WaybillForm(forms.ModelForm):
    class Meta:
        model = Waybill
        fields = [
            'sender_name', 'sender_phone',
            'receiver_name', 'receiver_phone',
            'origin', 'destination',
            'description', 'weight', 'trip'
        ]
        widgets = {
            'sender_name': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Sender full name'}),
            'sender_phone': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': '08012345678'}),
            'receiver_name': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Receiver full name'}),
            'receiver_phone': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': '08012345678'}),
            'origin': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'e.g. Jos'}),
            'destination': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'e.g. Lagos'}),
            'description': forms.Textarea(attrs={'class': INPUT_CLASS, 'rows': 3, 'placeholder': 'Describe the item(s)'}),
            'weight': forms.NumberInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Weight in kg', 'step': '0.1', 'min': '0.1'}),
            'trip': forms.Select(attrs={'class': INPUT_CLASS}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['trip'].queryset = Trip.objects.filter(status__in=['scheduled', 'boarding'])
        self.fields['trip'].required = False
        self.fields['trip'].label = 'Assign to Trip (optional)'

class TrackingForm(forms.Form):
    tracking_code = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': 'Enter tracking code e.g. WBXXXXXXXX',
            'style': 'text-transform: uppercase'
        })
    )

class WaybillStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = WaybillStatusHistory
        fields = ['status', 'note']
        widgets = {
            'status': forms.Select(attrs={'class': INPUT_CLASS}),
            'note': forms.Textarea(attrs={'class': INPUT_CLASS, 'rows': 2}),
        }
