from django import forms
from .models import Plant, Category
 
 
class PlantForm(forms.ModelForm):
 
    class Meta:
        model = Plant
        fields = ['name', 'description', 'image', 'is_edible']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Plant name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description', 'rows': 4}),
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'is_edible': forms.CheckboxInput(),
            }
 
    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError("Plant name must be at least 2 characters.")
        return name

    def clean_description(self):
        desc = self.cleaned_data.get('description', '').strip()
        if not desc:
            raise forms.ValidationError("Description is required.")
        return desc
 
 
class PlantFilterForm(forms.Form):
    name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search by plant name...'}),
    )
    is_edible = forms.NullBooleanField(
        required=False,
        widget=forms.Select(
            choices=[('', 'All Plants'), ('true', 'Edible'), ('false', 'Non-Edible')],
        )
    )