import os
import sys
import django
import pycountry

# Setup Django environment
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Planteer'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Planteer.settings')
django.setup()

from plants.models import Country

def seed_countries():
    for c in pycountry.countries:
        Country.objects.get_or_create(
            code=c.alpha_2,
            name=c.name
        )
    print("Countries seeded")

if __name__ == '__main__':
    seed_countries()
