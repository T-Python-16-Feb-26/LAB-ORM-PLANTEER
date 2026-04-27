from django.shortcuts import render, redirect
from plants.models import Plant
from .models import Contact
from .forms import ContactForm
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib import messages

def home_view(request):
    plants = Plant.objects.all()
    return render(request, 'main/index.html', {"plants": plants})

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
                    #send confirmation email
            content_html = ("yoooo")
            send_to = request.POST.get('email')
            email_message = EmailMessage("confiramation","hiiii",  settings.EMAIL_HOST_USER, [send_to])
            email_message.content_subtype = "html"
            #email_message.connection = email_message.get_connection(True)
            email_message.send()
            return redirect('main:contact_messages')
    else:
        form = ContactForm()
    return render(request, 'main/contact.html', {"form": form})

def contact_messages_view(request):
    contact_messages = Contact.objects.all().order_by('-created_at')
    return render(request, 'main/contact-messages.html', {"contact_messages": contact_messages})