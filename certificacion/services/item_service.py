import logging
from django.utils import timezone
from django.conf import settings
from certificacion.models import Item, Orden
from certificacion.validators import validate_item_data
from .orden_service import calculate_delivery_date

logger = logging.getLogger(__name__)

def save_item(orden, data):
    """
    Validates and saves a new item to an order.
    Recalculates the order's estimated delivery date.
    """
    validate_item_data(data)

    item = Item.objects.create(orden=orden, **data)
    logger.info(f"Item {item.id} created for order {orden.numero_orden}")

    calculate_estimated_time(orden)
    return item

def update_item(item, data):
    """
    Validates and updates an existing item.
    Recalculates the order's estimated delivery date.
    """
    validate_item_data(data)

    for key, value in data.items():
        setattr(item, key, value)
    item.save()

    calculate_estimated_time(item.orden)
    return item

def calculate_estimated_time(orden):
    """
    Recalculates the estimated delivery date for an order based on its items.
    """
    total_hours = 0
    for item in orden.items.all():
        base_hours = sum(settings.TIEMPOS_ETAPA.values())
        if item.tipo_item == 'Lote de gemas':
            total_hours += base_hours * 1.5
        elif item.tipo_item == 'Set de joyas':
            total_hours += base_hours * item.cantidad
        else:
            total_hours += base_hours

    new_delivery_date = calculate_delivery_date(orden.fecha_creacion)

    if orden.fecha_entrega_sugerida != new_delivery_date:
        orden.fecha_entrega_sugerida = new_delivery_date
        orden.save(update_fields=['fecha_entrega_sugerida'])
        logger.info(f"Updated delivery date for order {orden.numero_orden} to {new_delivery_date}")

    return new_delivery_date
