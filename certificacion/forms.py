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

    def clean(self):
        cleaned_data = super().clean()
        tipo_item = cleaned_data.get("tipo_item")

        required_fields = {
            'Piedras sueltas': ['color_gema', 'peso', 'cantidad'],
            'Lote de gemas': ['tipo_gema', 'cantidad_total', 'peso_promedio'],
            'Joya': ['tipo_joya', 'material_joya', 'color_gema', 'peso'],
            'Set de joyas': ['tipos_joya', 'material_joya', 'cantidad']
        }

        if tipo_item in required_fields:
            for field in required_fields[tipo_item]:
                if cleaned_data.get(field) is None:
                    self.add_error(field, 'Este campo es requerido.')

        if tipo_item == 'Piedras sueltas':
            cantidad = cleaned_data.get('cantidad')
            if cantidad is not None and not 1 <= cantidad <= 6:
                self.add_error('cantidad', 'La cantidad debe estar entre 1 y 6.')

        return cleaned_data
