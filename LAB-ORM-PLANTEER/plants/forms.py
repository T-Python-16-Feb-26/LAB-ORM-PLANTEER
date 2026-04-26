from django import forms
from .models import Plant


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['name', 'about', 'used_for', 'image', 'category', 'is_edible', 'countries']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter plant name'
            }),
            'about': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write information about the plant'
            }),
            'used_for': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'What is this plant used for?'
            }),
            'image': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Paste image URL'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'is_edible': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'countries': forms.SelectMultiple(attrs={
                'class': 'form-control'
            }),
        }

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if len(name) < 2:
            raise forms.ValidationError("Plant name must be at least 2 characters.")
        return name

    def clean_about(self):
        about = self.cleaned_data['about'].strip()
        if len(about) < 10:
            raise forms.ValidationError("About field must be at least 10 characters.")
        return about