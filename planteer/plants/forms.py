from django import forms
from .models import Plant, Country

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['name', 'about', 'used_for', 'image', 'category', 'is_edible','countries']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'about': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'used_for': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'countries': forms.SelectMultiple(attrs={'class': 'form-select'}),

            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_edible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
