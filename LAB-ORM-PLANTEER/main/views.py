from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import Contact
from plants.models import Plant


def home_view(request):
    latest_plants = Plant.objects.all().order_by('-created_at')[:6]
    return render(request, 'main/home.html', {'latest_plants': latest_plants})


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:contact_messages_view')
    else:
        form = ContactForm()

    return render(request, 'main/contact.html', {'form': form})


def contact_messages_view(request):
    messages = Contact.objects.all().order_by('-created_at')
    return render(request, 'main/contact_messages.html', {'messages': messages})