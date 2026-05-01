from django import forms
from contact.models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "required": True, "minlength": 3}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "required": True, "minlength": 3}),
            "email": forms.EmailInput(attrs={"class": "form-control", "required": True}),
            "message": forms.Textarea(attrs={"class": "form-control", "required": True, "rows": 5, "minlength": 10}),
        }