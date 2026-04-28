from django.shortcuts import render
from plants.models import Plant
from django.shortcuts import render, redirect
from .models import Contact
 


# Create your views here.

def home_view(request):
    return render(request, 'core/home.html')

def contact_view(request):
    return render(request, 'core/contact.html')


def home(request):
    plants = Plant.objects.all()[:3]
    recent_plants = Plant.objects.all().order_by('-created_at')[:3]

    return render(request, 'core/home.html', {
        'plants': plants,
        'recent_plants': recent_plants,
    })



def contact(request):
    errors = []
    form_data = {}

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        form_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'message': message,
        }

        if not first_name:
            errors.append('First name is required')
        if not last_name:
            errors.append('Last name is required')
        if not email or '@' not in email:
            errors.append('Valid email is required')
        if not message:
            errors.append('Message is required')

        if not errors:
            Contact.objects.create(**form_data)
            return redirect('/contact/?sent=1')

    return render(request, 'core/contact.html', {
        'errors': errors,
        'form_data': form_data,
    })

def messages_view(request):
    contacts = Contact.objects.all().order_by('-created_at')

    return render(request, 'core/messages.html', {
        'contacts': contacts
    })





def toggle_dark_mode(request):
    redirect_url = request.GET.get('next', '/')
    response = redirect(redirect_url)
    
    current = request.COOKIES.get('dark_mode', 'off')
    if current == 'on':
        response.set_cookie('dark_mode', 'off', max_age=60*60*24*30)
    else:
        response.set_cookie('dark_mode', 'on', max_age=60*60*24*30)
    
    return response


def care_tips_view(request):
    return render(request, 'core/care_tips.html')


ARTICLES = {
    'watering-guide': {
        'title': 'The Complete Watering Guide for Houseplants',
        'tag': 'Watering',
        'author': 'Lily',
        'read_time': '7 min read',
        'date': 'Mar 12',
        'image': 'https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=1200',
        'content': [
            {'heading': 'The Golden Rule', 'text': 'Never water on a schedule. Always check the soil moisture first by sticking your finger 2 inches into the soil. If it feels dry, water deeply. If still moist, wait another day or two.'},
            {'heading': 'How to Water Correctly', 'text': 'Water slowly and deeply until it drains from the bottom. This encourages roots to grow downward. Avoid shallow watering which leads to weak root systems.'},
            {'heading': 'Common Mistakes', 'text': 'Overwatering is the number one killer of houseplants. Signs include yellowing leaves, mushy stems, and soggy soil. Underwatering shows as dry, crispy leaf edges and wilting.'},
            {'heading': 'Water Quality', 'text': 'Most plants prefer room temperature water. Let tap water sit overnight to allow chlorine to evaporate. Rainwater or filtered water is ideal for sensitive plants like orchids.'},
        ]
    },
    'repotting-guide': {
        'title': 'When & How to Repot Your Plants the Right Way',
        'tag': 'Repotting',
        'author': 'Marcus',
        'read_time': '8 min read',
        'date': 'Mar 28',
        'image': 'https://images.unsplash.com/photo-1466692476868-aef1dfb1e735?w=1200',
        'content': [
            {'heading': 'When to Repot', 'text': 'Signs your plant needs repotting: roots growing out of drainage holes, plant drying out too quickly, or roots circling the bottom of the pot. Spring is the best time to repot.'},
            {'heading': 'Choosing the Right Pot', 'text': 'Always go up just one size — about 2 inches larger in diameter. Too large a pot holds excess moisture and can lead to root rot.'},
            {'heading': 'The Repotting Process', 'text': 'Water your plant the day before. Gently remove it, shake off old soil, trim any dead roots, and place in fresh potting mix. Water lightly after repotting.'},
            {'heading': 'After Care', 'text': 'Keep the plant in indirect light for 1-2 weeks after repotting. Avoid fertilizing for at least a month to let roots settle in the new soil.'},
        ]
    },
    'soil-guide': {
        'title': 'The Best Soil Mixes for Every Plant Type',
        'tag': 'Soil & Nutrients',
        'author': 'Lily',
        'read_time': '6 min read',
        'date': 'Apr 2',
        'image': 'https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=1200',
        'content': [
            {'heading': 'Why Soil Matters', 'text': 'Soil is the foundation of plant health. It provides nutrients, support, and regulates moisture. Using the wrong soil type is one of the most common mistakes.'},
            {'heading': 'For Succulents & Cacti', 'text': 'Use a fast-draining mix with extra perlite or coarse sand. Standard potting soil retains too much moisture and will cause root rot in succulents.'},
            {'heading': 'For Tropical Plants', 'text': 'A rich, well-draining mix works best. Combine potting soil with perlite and orchid bark for good aeration and moisture retention.'},
            {'heading': 'For Herbs', 'text': 'Herbs prefer a light, fertile mix with good drainage. Add compost for extra nutrients. Avoid heavy clay soils that compact easily.'},
        ]
    },
    'propagation-guide': {
        'title': 'How to Propagate Any Plant at Home',
        'tag': 'Propagation',
        'author': 'Sara',
        'read_time': '5 min read',
        'date': 'Apr 8',
        'image': 'https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?w=1200',
        'content': [
            {'heading': 'What is Propagation', 'text': 'Propagation is growing new plants from an existing one. It is free, fun, and a great way to expand your collection or share plants with friends.'},
            {'heading': 'Stem Cuttings', 'text': 'Cut a healthy stem just below a node. Remove lower leaves and place in water or moist soil. Keep in bright indirect light and change water every few days.'},
            {'heading': 'Leaf Cuttings', 'text': 'Perfect for succulents. Gently twist a healthy leaf off and lay it on top of dry soil. Mist lightly every few days until roots and a new plant emerge.'},
            {'heading': 'Division', 'text': 'For clumping plants, remove from pot and gently separate the root ball into sections. Each section should have roots and leaves. Pot up separately.'},
        ]
    },
    'seasonal-guide': {
        'title': 'Seasonal Plant Care: What to Do Each Month',
        'tag': 'Seasonal',
        'author': 'Marcus',
        'read_time': '9 min read',
        'date': 'Apr 15',
        'image': 'https://images.unsplash.com/photo-1534710961216-75c88202f43e?w=1200',
        'content': [
            {'heading': 'Spring (Mar-May)', 'text': 'This is the growing season. Start fertilizing, repot if needed, and increase watering as days get longer. Great time to take cuttings and propagate.'},
            {'heading': 'Summer (Jun-Aug)', 'text': 'Watch for heat stress and increase humidity. Water more frequently but check soil first. Move plants away from hot windows to avoid leaf scorch.'},
            {'heading': 'Autumn (Sep-Nov)', 'text': 'Gradually reduce watering and stop fertilizing. Bring outdoor plants inside before temperatures drop. Check for pests before bringing them indoors.'},
            {'heading': 'Winter (Dec-Feb)', 'text': 'Most plants go dormant. Water sparingly and avoid fertilizing. Keep plants away from cold drafts and heating vents. Dust leaves to maximize light absorption.'},
        ]
    },
}

def article_view(request, slug):
    article = ARTICLES.get(slug)
    if not article:
        return redirect('/care-tips/')
    return render(request, 'core/article.html', {'article': article})

def find_my_plant_view(request):
    return render(request, 'core/find_my_plant.html')

def find_my_plant_results(request):
    light = request.GET.get('light')
    water = request.GET.get('water')
    care = request.GET.get('care')

    from plants.models import Plant
    plants = Plant.objects.all()

    if light:
        plants = plants.filter(light=light)
    if water:
        plants = plants.filter(water=water)
    if care:
        plants = plants.filter(care_level=care)

    return render(request, 'core/find_my_plant_results.html', {
        'plants': plants,
        'light': light,
        'water': water,
        'care': care,
    })


def favourites_view(request):
    from plants.models import Plant
    favs = request.COOKIES.get('favs', '')
    fav_ids = [f for f in favs.split(',') if f]
    plants = Plant.objects.filter(id__in=fav_ids)
    return render(request, 'core/favourites.html', {'plants': plants})


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'core/register.html', {'error': 'Username already exists'})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        login(request, user)
        return redirect('/')

    return render(request, 'core/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'core/login.html', {'error': 'Invalid username or password'})

    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('/')
