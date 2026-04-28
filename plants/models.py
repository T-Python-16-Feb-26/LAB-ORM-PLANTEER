from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100)
    flag = models.ImageField(upload_to="countries/")

    def __str__(self):
        return self.name

class Plant(models.Model):
    class CategoryChoices(models.TextChoices):
        INDOOR = "indoor", "Indoor"
        OUTDOOR = "outdoor", "Outdoor"
        EDIBLE = "edible", "Edible"
        ORNAMENTAL = "ornamental", "Ornamental"

    name = models.CharField(max_length=100)
    about = models.TextField()
    used_for = models.TextField()
    image = models.ImageField(upload_to="plants/", blank=True, null=True)
    category = models.CharField(max_length=20, choices=CategoryChoices.choices)
    is_edible = models.BooleanField(default=False)
    light_requirement = models.CharField(max_length=100)
    watering = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    countries = models.ManyToManyField(Country, related_name="plants", blank=True)

    def __str__(self):
        return self.name
    
from django.contrib.auth.models import User

class Comment(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.plant.name}"