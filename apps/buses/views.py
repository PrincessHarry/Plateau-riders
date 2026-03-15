from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Bus
from .forms import BusForm

@login_required
def bus_list(request):
    buses = Bus.objects.all()
    return render(request, 'buses/bus_list.html', {'buses': buses})

@login_required
def bus_create(request):
    form = BusForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Bus added successfully.')
        return redirect('bus_list')
    return render(request, 'buses/bus_form.html', {'form': form, 'title': 'Add New Bus'})
