from django.shortcuts import render, redirect
from .models import ContactMessage
from django.contrib import messages

# Create your views here.
def contact_view(request):
    if request.method == "POST":
        data = {
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'email': request.POST.get('email'),
            'message': request.POST.get('message'),
        }
        
        ContactMessage.objects.create(**data)
        
        messages.success(request, "تم استلام رسالتك بنجاح!")
        return redirect('contact:contact_view')

    return render(request, 'contact/contact.html')


def messages_view(request):
    all_messages = ContactMessage.objects.all().order_by('-created_at')
    
    return render(request, 'contact/messages.html', {
        'user_messages': all_messages
    })