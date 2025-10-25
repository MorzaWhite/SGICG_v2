from django.core.exceptions import ValidationError

def validate_item_data(data):
    """
    Validates item data based on its type and other business rules.
    Raises ValidationError if the data is invalid.
    """
    errors = {}
    tipo_item = data.get('tipo_item')

    if not tipo_item:
        errors['tipo_item'] = "Este campo es requerido."
        raise ValidationError(errors)

    required_fields = {
        'Piedras sueltas': ['color_gema', 'peso', 'cantidad'],
        'Lote de gemas': ['tipo_gema', 'cantidad_total', 'peso_promedio'],
        'Joya': ['tipo_joya', 'material_joya', 'color_gema', 'peso'],
        'Set de joyas': ['tipos_joya', 'material_joya', 'cantidad']
    }

    if tipo_item in required_fields:
        for field in required_fields[tipo_item]:
            if not data.get(field):
                errors[field] = 'Este campo es requerido.'

    if tipo_item == 'Piedras sueltas':
        cantidad = data.get('cantidad')
        if cantidad is not None and not 1 <= int(cantidad) <= 6:
            errors['cantidad'] = 'La cantidad debe estar entre 1 y 6.'

    if tipo_item == 'Lote de gemas':
        cantidad_total = data.get('cantidad_total')
        peso_promedio = data.get('peso_promedio')
        if peso_promedio and float(peso_promedio) > 0 and (not cantidad_total or int(cantidad_total) <= 0):
            errors['cantidad_total'] = 'La cantidad total debe ser mayor que cero si hay un peso promedio.'

    if errors:
        raise ValidationError(errors)

    return data
