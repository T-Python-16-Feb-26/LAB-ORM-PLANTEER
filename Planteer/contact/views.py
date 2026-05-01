from django.shortcuts import get_object_or_404, render , redirect
from django.http import HttpRequest, HttpResponse
from .models import Contact
from .forms import ContactForm

# Create your views here.

def contact_view(request: HttpRequest) :
     
    if request.method == "POST":
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            return redirect('contact:message_view')
    else:
        contact_form = ContactForm()
        return render(request, 'contact/contact_page.html', {'form': contact_form})

    return render(request, "contact/contact_page.html")

def message_view(request: HttpRequest):
    messages = Contact.objects.all().order_by("-created_at")
    return render(request, "contact/message_page.html", {"messages": messages})