from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Route, RouteStop
from .forms import RouteForm, RouteStopFormSet

@login_required
def route_list(request):
    routes = Route.objects.prefetch_related('stops').all()
    return render(request, 'routes/route_list.html', {'routes': routes})

@login_required
def route_create(request):
    form = RouteForm(request.POST or None)
    if form.is_valid():
        route = form.save()
        messages.success(request, 'Route created successfully.')
        return redirect('route_stops', pk=route.pk)
    return render(request, 'routes/route_form.html', {'form': form})

@login_required
def route_stops(request, pk):
    route = get_object_or_404(Route, pk=pk)
    if request.method == 'POST':
        formset = RouteStopFormSet(request.POST, instance=route)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Route stops saved.')
            return redirect('route_list')
    else:
        formset = RouteStopFormSet(instance=route)
    return render(request, 'routes/route_stops.html', {'route': route, 'formset': formset})
