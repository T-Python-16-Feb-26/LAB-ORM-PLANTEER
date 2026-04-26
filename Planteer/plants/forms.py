from django import forms
from .models import Plant

class PlantForm(forms.ModelForm):
    name = forms.CharField(
        min_length=3, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Plant Name'})
    )
    about = forms.CharField(
        min_length=20, 
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write at least 20 characters...'})
    )

    class Meta:
        model = Plant
        fields = "__all__"
       
        widgets = {
            'used_for': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Usage details...'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'is_edible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'countries': forms.MultipleHiddenInput(),
            
        }