from django import forms
from .models import Orden, TipoJoya, MaterialJoya, Item

class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ['numero_orden', 'tags']
        widgets = {
            'numero_orden': forms.TextInput(attrs={'class': 'form-control'}),
            'tags': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'tags', 'tipo_certificado', 'tipo_item', 'color_gema', 'peso', 'cantidad',
            'cantidad_total', 'tipo_gema', 'peso_promedio', 'tipo_joya',
            'material_joya', 'tipos_joya', 'tiene_seguro'
        ]
        widgets = {
            'tags': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tipo_certificado': forms.Select(attrs={'class': 'form-control'}),
            'tipo_item': forms.Select(attrs={'class': 'form-control'}),
            'color_gema': forms.TextInput(attrs={'class': 'form-control'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidad_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_gema': forms.TextInput(attrs={'class': 'form-control'}),
            'peso_promedio': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_joya': forms.Select(attrs={'class': 'form-control'}),
            'material_joya': forms.Select(attrs={'class': 'form-control'}),
            'tipos_joya': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'tiene_seguro': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
