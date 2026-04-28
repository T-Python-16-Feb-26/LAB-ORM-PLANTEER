

import os
import sys
import django
import pycountry

# Setup Django environment
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Planteer'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Planteer.settings')
django.setup()

from plants.models import Plant, Category, Country
from django.core.files import File



DATA_DIR = os.path.dirname(__file__)
IMAGES_DIR = os.path.join(DATA_DIR, 'images')
TXT_FILE = os.path.join(DATA_DIR, 'plants_info.txt')
for plant in Plant.objects.all():
    if plant.image:
        if os.path.isfile(plant.image.path):
            os.remove(plant.image.path)
Plant.objects.all().delete()
Category.objects.all().delete()

def parse_plants(filepath):
    plants = []
    current = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                if current:
                    plants.append(current)
                    current = {}
                continue
            if ': ' in line:
                key, _, value = line.partition(': ')
                current[key.strip()] = value.strip()
    if current:
        plants.append(current)
    return plants


def seed():
    plants = parse_plants(TXT_FILE)
    for data in plants:
        name        = data.get('Name')
        about       = data.get('about')
        used_for    = data.get('used_for')
        image_path  = data.get('image', '').lstrip('/')
        category    = data.get('Category')

        is_edible   = data.get('is_edible', 'False').strip().lower() == 'true'
        country_names = [c.strip() for c in data.get('Country', '').split(',') if c.strip()]

        if Plant.objects.filter(name=name).exists():
            print(f'Skipping "{name}" — already exists.')
            continue

        cat_obj, _ = Category.objects.get_or_create(name=category)
        plant = Plant(name=name, about=about, used_for=used_for, is_edible=is_edible)

        abs_image = os.path.join(IMAGES_DIR, image_path)
        if os.path.exists(abs_image):
            with open(abs_image, 'rb') as img_file:
                plant.image.save(os.path.basename(abs_image), File(img_file), save=False)
        else:
            print(f'  Warning: image not found at {abs_image}, using default.')


        plant.save()
        plant.categories.add(cat_obj)

        # Add countries (link only, never create)
        country_objs = []
        for cname in country_names:
            try:
                code = pycountry.countries.lookup(cname).alpha_2
                country = Country.objects.get(code=code)
                country_objs.append(country)
            except Exception:
                print(f"Warning: country not found -> {cname}")
        if country_objs:
            plant.countries.set(country_objs)

        print(f'Added "{name}".')

    print('Done.')


if __name__ == '__main__':
    seed()
