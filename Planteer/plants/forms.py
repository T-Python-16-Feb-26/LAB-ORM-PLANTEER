from django import forms
from plants.models import Plant

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['name_plant', 'used_for', 'about', 'image', 'category', 'is_edible','countries']