from django import forms
from .models import Contact
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already used.")

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        return user


class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "placeholder": "Enter your email"
        })
    )

    def clean(self):
        email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if email and password:
            try:
                user = User.objects.get(email=email)
                self.cleaned_data["username"] = user.username
            except User.DoesNotExist:
                raise forms.ValidationError("Invalid email or password.")

        return super().clean()



class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'message']

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First name',
                'required': True,
                'minlength': 2,
                'maxlength': 100,
            }),

            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last name',
                'required': True,
                'minlength': 2,
                'maxlength': 100,
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email address',
                'required': True,
                'maxlength': 150,
            }),

            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your message',
                'rows': 5,
                'required': True,
                'minlength': 10,
                'maxlength': 1000,
            }),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', '').strip()

        if len(first_name) < 2:
            raise forms.ValidationError(
                'First name must be at least 2 characters.'
            )

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name', '').strip()

        if len(last_name) < 2:
            raise forms.ValidationError(
                'Last name must be at least 2 characters.'
            )

        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()

        if '@' not in email:
            raise forms.ValidationError(
                'Please enter a valid email address.'
            )

        return email

    def clean_message(self):
        message = self.cleaned_data.get('message', '').strip()

        if len(message) < 10:
            raise forms.ValidationError(
                'Message must be at least 10 characters.'
            )

        return message