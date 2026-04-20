from django import forms
from .models import ContactMessage
 
 
class ContactForm(forms.ModelForm):
 
    class Meta:
        model = ContactMessage
        fields = ['first_name', 'last_name', 'email', 'message']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Jane', 'required': True}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Smitherton', 'required': True}),
            'email': forms.EmailInput(attrs={'placeholder': 'email@fakedomain.net', 'required': True}),
            'message': forms.Textarea(attrs={'placeholder': 'Enter your question or message', 'rows': 5, 'required': True}),
        }
 
    def clean_first_name(self):
        name = self.cleaned_data.get('first_name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError("First name must be at least 2 characters.")
        return name
 
    def clean_message(self):
        msg = self.cleaned_data.get('message', '').strip()
        if len(msg) < 10:
            raise forms.ValidationError("Message must be at least 10 characters.")
        return msg