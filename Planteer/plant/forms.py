from django import forms
from plant.models import Plant

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control","required": True ,"minlength": 3}),
            "about": forms.Textarea(attrs={"class": "form-control", "required": True, "rows": 3, "minlength": 10}),
            "used_for": forms.Textarea(attrs={"class": "form-control", "required": True, "rows": 3 ,"minlength": 10}),
            "category": forms.Select(attrs={"class": "form-control", "required": True}), 
            "is_edible": forms.CheckboxInput(attrs={"class": "form-check-input", "required": False}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control-file", "required": False, "accept": "image/*"}),
            "countries":  forms.CheckboxSelectMultiple(),
        }