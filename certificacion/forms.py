from django import forms
from .models import Orden, TipoJoya, MaterialJoya, Item

class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = [
            'tiene_seguro',
            'tags',
        ]
        widgets = {
            'tiene_seguro': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tags': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'tipo_certificado', 'tipo_item', 'color_gema', 'peso', 'cantidad',
            'cantidad_total', 'tipo_gema', 'peso_promedio', 'tipo_joya',
            'material_joya', 'tipos_joya'
        ]
        widgets = {
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
        }

    def clean(self):
        cleaned_data = super().clean()
        tipo_certificado = cleaned_data.get("tipo_certificado")
        tipo_item = cleaned_data.get("tipo_item")

        if tipo_certificado == 'Verbal' and tipo_item == 'Lote de gemas':
            raise forms.ValidationError(
                "Un certificado 'Verbal' no puede ser emitido para un 'Lote de gemas'."
            )

        return cleaned_data
