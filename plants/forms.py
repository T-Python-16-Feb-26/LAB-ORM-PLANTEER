from django import forms
from .models import Plant

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = [
            'name',
            'about',
            'used_for',
            'light_requirement',
            'watering',
            'image',
            'category',
            'is_edible',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Plant name',
                'required': True,
                'minlength': 2,
                'maxlength': 100,
            }),
            'about': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write about the plant',
                'rows': 4,
                'required': True,
                'minlength': 10,
            }),
            'used_for': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'What is this plant used for?',
                'rows': 3,
                'required': True,
                'minlength': 5,
            }),
            'light_requirement': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Bright indirect light',
                'required': True,
                'minlength': 3,
            }),
            'watering': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Water once every 5 days',
                'required': True,
                'minlength': 3,
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
            'is_edible': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if not name:
            raise forms.ValidationError("Plant name is required.")

        name = name.strip()

        if len(name) < 2:
            raise forms.ValidationError("Plant name must be at least 2 characters.")

        return name

    def clean_about(self):
        about = self.cleaned_data.get('about')

        if not about:
            raise forms.ValidationError("About field is required.")

        about = about.strip()

        if len(about) < 10:
            raise forms.ValidationError("About must be at least 10 characters.")

        return about

    def clean_used_for(self):
        used_for = self.cleaned_data.get('used_for')

        if not used_for:
            raise forms.ValidationError("Used for field is required.")

        used_for = used_for.strip()

        if len(used_for) < 5:
            raise forms.ValidationError("Used for must be at least 5 characters.")

        return used_for

    def clean_light_requirement(self):
        light_requirement = self.cleaned_data.get('light_requirement')

        if not light_requirement:
            raise forms.ValidationError("Light requirement is required.")

        light_requirement = light_requirement.strip()

        if len(light_requirement) < 3:
            raise forms.ValidationError("Light requirement must be at least 3 characters.")

        return light_requirement

    def clean_watering(self):
        watering = self.cleaned_data.get('watering')

        if not watering:
            raise forms.ValidationError("Watering field is required.")

        watering = watering.strip()

        if len(watering) < 3:
            raise forms.ValidationError("Watering field must be at least 3 characters.")

        return watering