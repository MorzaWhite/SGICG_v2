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
    tipo_certificado = models.CharField(max_length=50, choices=TIPO_CERTIFICADO_CHOICES)
    color_gema = models.CharField(max_length=100)
    peso = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_joya = models.ForeignKey(TipoJoya, on_delete=models.SET_NULL, null=True, blank=True)
    material_joya = models.ForeignKey(MaterialJoya, on_delete=models.SET_NULL, null=True, blank=True)
    tiene_seguro = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_entrega_sugerida = models.DateTimeField()
    tags = models.TextField(blank=True)

    def __str__(self):
        return f"Orden {self.numero_orden}"
