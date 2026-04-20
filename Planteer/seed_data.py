"""
Seed script: adds real categories and plants with real images.
Run with: python manage.py shell < seed_data.py
"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planteer.settings')
django.setup()

from plants.models import Category, Plant

# ========== CATEGORIES ==========
categories_data = [
    {'name': 'Succulents', 'description': 'Drought-tolerant plants with thick, fleshy leaves that store water.'},
    {'name': 'Herbs', 'description': 'Aromatic plants used for cooking, medicine, and fragrance.'},
    {'name': 'Flowering Plants', 'description': 'Plants that produce beautiful and colorful flowers.'},
    {'name': 'Trees', 'description': 'Large woody plants with a single main trunk.'},
    {'name': 'Tropical Plants', 'description': 'Lush plants native to tropical climates.'},
    {'name': 'Vegetables', 'description': 'Edible plants grown for food and nutrition.'},
]

cats = {}
for c in categories_data:
    obj, created = Category.objects.get_or_create(name=c['name'], defaults=c)
    cats[c['name']] = obj
    print(f"{'Created' if created else 'Exists'}: {obj.name}")

# ========== PLANTS ==========
plants_data = [
    # --- Succulents ---
    {
        'name': 'Aloe Vera',
        'scientific_name': 'Aloe barbadensis miller',
        'description': 'Aloe vera is a succulent plant species known for its medicinal properties. The gel inside its leaves is widely used for treating burns, skin irritations, and is a popular ingredient in skincare products. It thrives in warm, dry climates and requires minimal watering.',
        'category': 'Succulents',
        'image_url': 'https://images.unsplash.com/photo-1509423350716-97f9360b4e09?w=600',
        'is_edible': True,
    },
    {
        'name': 'Echeveria',
        'scientific_name': 'Echeveria elegans',
        'description': 'Echeveria is a large genus of flowering plants in the family Crassulaceae, native to semi-desert areas of Central America. These rosette-forming succulents are popular houseplants due to their beautiful symmetrical shape and variety of colors from pale green to deep purple.',
        'category': 'Succulents',
        'image_url': 'https://images.unsplash.com/photo-1459411552884-841db9b3cc2a?w=600',
        'is_edible': False,
    },
    {
        'name': 'Jade Plant',
        'scientific_name': 'Crassula ovata',
        'description': 'The jade plant is a popular succulent houseplant with thick, woody stems and oval-shaped leaves. Often called the money plant or lucky plant, it is believed to bring good fortune. With proper care, jade plants can live for decades and even develop into small tree-like forms.',
        'category': 'Succulents',
        'image_url': 'https://images.unsplash.com/photo-1509937528035-ad76f8df97e1?w=600',
        'is_edible': False,
    },
    # --- Herbs ---
    {
        'name': 'Basil',
        'scientific_name': 'Ocimum basilicum',
        'description': 'Basil is a culinary herb of the family Lamiaceae. It is a tender plant used in cuisines worldwide, especially Italian cooking. Sweet basil has a strong, pungent, and sweet smell. It is an annual plant that thrives in warm, sunny conditions with regular watering.',
        'category': 'Herbs',
        'image_url': 'https://images.unsplash.com/photo-1618375569909-3c8616cf7733?w=600',
        'is_edible': True,
    },
    {
        'name': 'Rosemary',
        'scientific_name': 'Salvia rosmarinus',
        'description': 'Rosemary is a fragrant evergreen herb native to the Mediterranean. It is used as a culinary condiment, to make perfumes, and for its potential health benefits. The plant has needle-like leaves and produces small blue, purple, pink, or white flowers.',
        'category': 'Herbs',
        'image_url': 'https://images.unsplash.com/photo-1515586000433-45406d8e6662?w=600',
        'is_edible': True,
    },
    {
        'name': 'Mint',
        'scientific_name': 'Mentha spicata',
        'description': 'Mint is a fast-growing aromatic herb that is widely used in cooking, teas, and beverages. It has a refreshing cool flavor and is easy to grow. Be careful though — mint spreads aggressively and is best grown in containers to prevent it from taking over your garden.',
        'category': 'Herbs',
        'image_url': 'https://images.unsplash.com/photo-1628556270448-4d4e4148e1b1?w=600',
        'is_edible': True,
    },
    # --- Flowering Plants ---
    {
        'name': 'Lavender',
        'scientific_name': 'Lavandula angustifolia',
        'description': 'Lavender is a flowering plant in the mint family, known for its beautiful purple flowers and calming fragrance. It is widely used in aromatherapy, perfumes, and cooking. Lavender is drought-tolerant once established and attracts pollinators like bees and butterflies.',
        'category': 'Flowering Plants',
        'image_url': 'https://images.unsplash.com/photo-1468327768560-75b778cbb551?w=600',
        'is_edible': True,
    },
    {
        'name': 'Sunflower',
        'scientific_name': 'Helianthus annuus',
        'description': 'Sunflowers are tall, bright flowering plants that are known for their large, daisy-like flower heads. They follow the sun across the sky (heliotropism) when young. Sunflower seeds are edible and nutritious, and the plants can grow up to 3 meters tall.',
        'category': 'Flowering Plants',
        'image_url': 'https://images.unsplash.com/photo-1597848212624-a19eb35e2651?w=600',
        'is_edible': True,
    },
    {
        'name': 'Rose',
        'scientific_name': 'Rosa gallica',
        'description': 'Roses are woody perennial flowering plants known for their beauty and fragrance. They come in thousands of cultivars with various colors, sizes, and forms. Roses have cultural significance worldwide and are symbols of love and beauty. They require regular pruning and care.',
        'category': 'Flowering Plants',
        'image_url': 'https://images.unsplash.com/photo-1455659817273-f96807779a8a?w=600',
        'is_edible': False,
    },
    # --- Trees ---
    {
        'name': 'Olive Tree',
        'scientific_name': 'Olea europaea',
        'description': 'The olive tree is an evergreen tree native to the Mediterranean Basin. It is cultivated for its fruit (olives) which are used to produce olive oil. Olive trees are drought-resistant, can live for thousands of years, and are symbols of peace and prosperity.',
        'category': 'Trees',
        'image_url': 'https://images.unsplash.com/photo-1445282768818-728615cc910a?w=600',
        'is_edible': True,
    },
    {
        'name': 'Japanese Maple',
        'scientific_name': 'Acer palmatum',
        'description': 'Japanese maples are small deciduous trees known for their stunning autumn foliage. They come in hundreds of varieties with leaves ranging from deep red to bright green. These elegant trees are staples in Japanese gardens and make excellent ornamental specimens.',
        'category': 'Trees',
        'image_url': 'https://images.unsplash.com/photo-1509773896068-7fd415d91e2e?w=600',
        'is_edible': False,
    },
    # --- Tropical Plants ---
    {
        'name': 'Monstera',
        'scientific_name': 'Monstera deliciosa',
        'description': 'Monstera deliciosa, also known as the Swiss cheese plant, is a species of flowering plant native to tropical forests. It is famous for its large, glossy, heart-shaped leaves with natural holes (fenestrations). It is one of the most popular houseplants worldwide.',
        'category': 'Tropical Plants',
        'image_url': 'https://images.unsplash.com/photo-1614594975525-e45190c55d0b?w=600',
        'is_edible': False,
    },
    {
        'name': 'Bird of Paradise',
        'scientific_name': 'Strelitzia reginae',
        'description': 'The bird of paradise is a tropical plant known for its striking, crane-like flowers in orange and blue. Native to South Africa, it has become a popular ornamental plant in warm climates. The flowers resemble a colorful bird in flight, giving it its common name.',
        'category': 'Tropical Plants',
        'image_url': 'https://images.unsplash.com/photo-1603912699214-92627f304eb6?w=600',
        'is_edible': False,
    },
    # --- Vegetables ---
    {
        'name': 'Tomato',
        'scientific_name': 'Solanum lycopersicum',
        'description': 'The tomato is a widely grown edible berry of the nightshade family. Originating from western South America, it is now cultivated worldwide. Tomatoes are rich in vitamins C and K, potassium, and the antioxidant lycopene. They are a staple in countless cuisines.',
        'category': 'Vegetables',
        'image_url': 'https://images.unsplash.com/photo-1592841200221-a6898f307baa?w=600',
        'is_edible': True,
    },
    {
        'name': 'Chili Pepper',
        'scientific_name': 'Capsicum annuum',
        'description': 'Chili peppers are fruits of plants from the genus Capsicum, members of the nightshade family. They are widely used as a spice to add heat and flavor to dishes worldwide. Chili peppers contain capsaicin, which gives them their characteristic spicy taste.',
        'category': 'Vegetables',
        'image_url': 'https://images.unsplash.com/photo-1583119022894-919a68a3d0e3?w=600',
        'is_edible': True,
    },
]

for p_data in plants_data:
    cat_name = p_data.pop('category')
    p_data['category'] = cats[cat_name]
    obj, created = Plant.objects.get_or_create(name=p_data['name'], defaults=p_data)
    print(f"{'Created' if created else 'Exists'}: {obj.name} ({cat_name})")

print(f"\nDone! {Plant.objects.count()} plants and {Category.objects.count()} categories in the database.")