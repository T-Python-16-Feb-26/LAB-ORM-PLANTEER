from django.db import models
from django.contrib.auth.models import User

class Country(models.Model):
    name = models.CharField(max_length=100)
    flag = models.ImageField(upload_to='flags/', null=True, blank=True)

    def __str__(self):
        return self.name


class Plant(models.Model):

    class Category(models.TextChoices):
       TR = 'TR', 'Tropical'
       SU = 'SU', 'Succulents'
       HE = 'HE', 'Herbs'
       FE = 'FE', 'Ferns'
       FL = 'FL', 'Flowering'
       TRS = 'TRS', 'Trees'

    class WaterLevel(models.TextChoices):
        LOW = 'LOW', 'Low'
        MODERATE = 'MO', 'Moderate'
        HIGH = 'HIGH', 'High'

    class LightLevel(models.TextChoices):
        DIRECT = 'DIR', 'Direct'
        INDIRECT = 'IND', 'Indirect'
        LOW_LIGHT = 'LOW', 'Low Light'

    class CareLevel(models.TextChoices):
        EASY = 'EASY', 'Easy'
        MEDIUM = 'MED', 'Medium'
        HARD = 'HARD', 'Hard'

    name = models.CharField(max_length=200)
    about = models.TextField()
    used_for = models.TextField()
    image = models.ImageField(upload_to='plants/', null=True, blank=True)
    category = models.CharField(max_length=20, choices=Category.choices)
    is_edible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    countries = models.ManyToManyField(Country, blank=True, related_name='plants')
    water = models.CharField(max_length=10, choices=WaterLevel.choices, null=True, blank=True)
    light = models.CharField(max_length=10, choices=LightLevel.choices, null=True, blank=True)
    care_level = models.CharField(max_length=10, choices=CareLevel.choices, null=True, blank=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.plant.name}"
    

