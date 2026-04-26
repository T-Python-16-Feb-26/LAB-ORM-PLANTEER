from django import forms
from plants.models import Plant

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = [
            'name',
            'about',
            'used_for',
            'category',
            'light',
            'care_level',
            'image'
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'about': forms.Textarea(attrs={'class': 'form-control'}),
            'used_for': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'light': forms.Select(attrs={'class': 'form-control'}),
            'care_level': forms.Select(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': 'Plant Name',
            'about': 'Description',
            'used_for': 'Used For',
            'category': 'Category',
            'light': 'Light Requirement',
            'care_level': 'Care Level',
            'image': 'Plant Image',
        }
        
        