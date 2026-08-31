from django.http import HttpRequest
from django.contrib import messages
from django.shortcuts import redirect, render

from .models import Contact
from plants.models import Plant

def home_view(request: HttpRequest):

    latest_plants = Plant.objects.order_by('-created_at')[:3]
    return render(request, 'main/index.html', {'latest_plants': latest_plants})

def contact_view(request: HttpRequest):
    if request.method == 'POST':
        Contact.objects.create(
            first_name=request.POST.get('first_name', '').strip(),
            last_name=request.POST.get('last_name', '').strip(),
            email=request.POST.get('email', '').strip(),
            message=request.POST.get('message', '').strip(),
        )
        messages.success(request, 'Your message has been sent successfully.')
        return redirect('main:contact_view')

    return render(request, 'main/contact.html')

def contact_messages_view(request: HttpRequest):
    contact_messages = Contact.objects.order_by('-created_at')
    return render(request, 'main/contact_messages.html', {'contact_messages': contact_messages})


