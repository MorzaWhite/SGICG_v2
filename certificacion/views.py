from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.utils import timezone
import json
from .forms import OrdenForm, ItemForm
from .models import Orden, Item
from .services.orden_service import calculate_delivery_date
from .services import item_service

def crear_orden(request):
    if request.method == 'POST':
        form = OrdenForm(request.POST)
        if form.is_valid():
            orden = form.save(commit=False)
            orden.fecha_creacion = timezone.now()
            orden.fecha_entrega_sugerida = calculate_delivery_date(orden.fecha_creacion)
            orden.save()
            return redirect('crear_item', orden_id=orden.id)
    else:
        form = OrdenForm()
    return render(request, 'certificacion/crear_orden.html', {'form': form})

def crear_item(request, orden_id):
    orden = get_object_or_404(Orden, id=orden_id)
    form = ItemForm(initial={'tags': orden.tags})
    return render(request, 'certificacion/crear_item.html', {'form': form, 'orden': orden})

@csrf_exempt
def item_api_view(request, orden_id, item_id=None):
    orden = get_object_or_404(Orden, id=orden_id)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item = item_service.save_item(orden, data)
            return JsonResponse({'status': 'success', 'item_id': item.id}, status=201)
        except ValidationError as e:
            return JsonResponse({'status': 'error', 'errors': e.message_dict}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    if request.method == 'GET':
        items = Item.objects.filter(orden=orden).values()
        return JsonResponse(list(items), safe=False)

    if request.method == 'PUT':
        if not item_id:
            return JsonResponse({'status': 'error', 'message': 'Item ID is required for updates.'}, status=400)
        try:
            item = get_object_or_404(Item, id=item_id, orden=orden)
            data = json.loads(request.body)
            item = item_service.update_item(item, data)
            return JsonResponse({'status': 'success', 'item_id': item.id})
        except ValidationError as e:
            return JsonResponse({'status': 'error', 'errors': e.message_dict}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)
