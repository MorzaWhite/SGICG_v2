from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .forms import OrdenForm, ItemForm
from .models import Orden
from .services.orden_service import get_next_order_number, calculate_delivery_date
from django.contrib import messages

def crear_orden(request):
    if request.method == 'POST':
        form = OrdenForm(request.POST)
        if form.is_valid():
            orden = form.save(commit=False)
            orden.numero_orden = get_next_order_number()
            orden.fecha_creacion = timezone.now()
            orden.fecha_entrega_sugerida = calculate_delivery_date(orden.fecha_creacion)
            orden.save()
            messages.success(request, f'Orden {orden.numero_orden} creada exitosamente.')
            return redirect('crear_item', orden_id=orden.id)
    else:
        form = OrdenForm()

    return render(request, 'certificacion/crear_orden.html', {'form': form})

def crear_item(request, orden_id):
    orden = get_object_or_404(Orden, id=orden_id)
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.orden = orden
            item.save()
            form.save_m2m()
            messages.success(request, f'Item agregado a la Orden {orden.numero_orden} exitosamente.')
            return redirect('crear_item', orden_id=orden.id)
    else:
        form = ItemForm()

    return render(request, 'certificacion/crear_item.html', {'form': form, 'orden': orden})
