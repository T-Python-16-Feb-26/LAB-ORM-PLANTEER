import pycountry
from .models import Country

for c in pycountry.countries:
    Country.objects.get_or_create(
        code=c.alpha_2,
        name=c.name
    )