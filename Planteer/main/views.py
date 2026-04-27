from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from plants.models import Plant, Category
from .forms import ContactForm
from .models import ContactMessage


def home(request: HttpRequest):
    featured_plants = Plant.objects.all()[:6]
    categories = Category.objects.all()

    return render(request, 'main/home.html', {
        'featured_plants': featured_plants,
        'categories': categories,
    })


def contact(request: HttpRequest):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'main/contact.html', {
                'form': ContactForm(),
                'success': True,
            })
    else:
        form = ContactForm()

    return render(request, 'main/contact.html', {'form': form})


def contact_messages(request: HttpRequest):
    messages_list = ContactMessage.objects.all()

    return render(request, 'main/contact_messages.html', {
        'messages_list': messages_list,
    })