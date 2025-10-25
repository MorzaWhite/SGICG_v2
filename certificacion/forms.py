from django import forms
from .models import Orden, TipoJoya, MaterialJoya

class OrdenForm(forms.ModelForm):
    tipo_joya = forms.ModelChoiceField(
        queryset=TipoJoya.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    material_joya = forms.ModelChoiceField(
        queryset=MaterialJoya.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Orden
        fields = [
            'tipo_certificado',
            'color_gema',
            'peso',
            'tipo_joya',
            'material_joya',
            'tiene_seguro',
            'tags',
        ]
        widgets = {
            'tipo_certificado': forms.Select(attrs={'class': 'form-control'}),
            'color_gema': forms.TextInput(attrs={'class': 'form-control'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control'}),
            'tiene_seguro': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tags': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
