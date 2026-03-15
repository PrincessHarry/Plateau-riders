from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Waybill, WaybillStatusHistory
from .forms import WaybillForm, TrackingForm, WaybillStatusUpdateForm

def create_waybill(request):
    form = WaybillForm(request.POST or None)
    if form.is_valid():
        waybill = form.save(commit=False)
        waybill.amount = waybill.calculate_amount()
        waybill.save()
        WaybillStatusHistory.objects.create(
            waybill=waybill,
            status='booked',
            note='Waybill created',
            updated_by=request.user.username if request.user.is_authenticated else 'System'
        )
        messages.success(request, f'Waybill created! Tracking code: {waybill.tracking_code}')
        return redirect('waybill_receipt', tracking_code=waybill.tracking_code)
    return render(request, 'waybill/create.html', {'form': form})

def track_parcel(request):
    form = TrackingForm(request.GET or None)
    waybill = None
    error = None
    if request.GET.get('tracking_code'):
        code = request.GET.get('tracking_code', '').upper().strip()
        try:
            waybill = Waybill.objects.prefetch_related('status_history').get(tracking_code=code)
        except Waybill.DoesNotExist:
            error = f'No parcel found with tracking code: {code}'
    return render(request, 'waybill/track.html', {'form': form, 'waybill': waybill, 'error': error})

def waybill_receipt(request, tracking_code):
    waybill = get_object_or_404(Waybill, tracking_code=tracking_code)
    return render(request, 'waybill/receipt.html', {'waybill': waybill})

@login_required
def waybill_list(request):
    waybills = Waybill.objects.all().order_by('-created_at')
    return render(request, 'waybill/list.html', {'waybills': waybills})

@login_required
def update_waybill_status(request, pk):
    waybill = get_object_or_404(Waybill, pk=pk)
    form = WaybillStatusUpdateForm(request.POST or None)
    if form.is_valid():
        history = form.save(commit=False)
        history.waybill = waybill
        history.updated_by = request.user.username
        history.save()
        waybill.status = history.status
        waybill.save()
        messages.success(request, 'Parcel status updated.')
        return redirect('waybill_list')
    return render(request, 'waybill/update_status.html', {'waybill': waybill, 'form': form})
