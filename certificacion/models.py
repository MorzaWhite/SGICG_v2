from django.db import models
from django.utils import timezone

class TipoJoya(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class MaterialJoya(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Orden(models.Model):
    TIPO_CERTIFICADO_CHOICES = [
        ('Verbal', 'Verbal'),
        ('Gem Card', 'Gem Card'),
        ('Escrito', 'Escrito'),
        ('Reimpresion', 'Reimpresión'),
        ('Verbal a Gem Card o Escrito', 'Verbal a Gem Card o Escrito'),
    ]

    numero_orden = models.PositiveIntegerField(unique=True, editable=False)
    tiene_seguro = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_entrega_sugerida = models.DateTimeField()
    tags = models.TextField(blank=True)

    def __str__(self):
        return f"Orden {self.numero_orden}"


class Item(models.Model):
    TIPO_CERTIFICADO_CHOICES = [
        ('Verbal', 'Verbal'),
        ('Gem Card', 'Gem Card'),
        ('Escrito', 'Escrito'),
        ('Reimpresion', 'Reimpresión'),
        ('Verbal a Gem Card o Escrito', 'Verbal a Gem Card o Escrito'),
    ]
    TIPO_ITEM_CHOICES = [
        ('Piedras sueltas', 'Piedras sueltas'),
        ('Lote de gemas', 'Lote de gemas'),
        ('Joya', 'Joya'),
        ('Set de joyas', 'Set de joyas'),
    ]

    orden = models.ForeignKey(Orden, related_name='items', on_delete=models.CASCADE)
    tipo_certificado = models.CharField(max_length=50, choices=TIPO_CERTIFICADO_CHOICES)
    tipo_item = models.CharField(max_length=50, choices=TIPO_ITEM_CHOICES)

    # Fields for 'Piedras sueltas'
    color_gema = models.CharField(max_length=100, blank=True)
    peso = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cantidad = models.PositiveIntegerField(null=True, blank=True)

    # Fields for 'Lote de gemas'
    cantidad_total = models.PositiveIntegerField(null=True, blank=True)
    tipo_gema = models.CharField(max_length=100, blank=True)
    peso_promedio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Fields for 'Joya' and 'Set de joyas'
    tipo_joya = models.ForeignKey(TipoJoya, on_delete=models.SET_NULL, null=True, blank=True)
    material_joya = models.ForeignKey(MaterialJoya, on_delete=models.SET_NULL, null=True, blank=True)

    # Field for 'Set de joyas' (multiple types of jewelry)
    tipos_joya = models.ManyToManyField(TipoJoya, related_name='items_set', blank=True)

    def __str__(self):
        return f"Item {self.id} de la Orden {self.orden.numero_orden}"
