from django.db import models
from django.contrib.auth.models import User
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    def __str__(self) -> str:
        return self.name

class Country(models.Model):
    code = models.CharField(max_length=2, unique=True)  # SA, US, etc
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

    def flag_url(self):
        return f"https://flagcdn.com/24x18/{self.code.lower()}.png"

class Plant(models.Model):
    name = models.CharField(max_length=1024)
    about = models.TextField()
    used_for = models.TextField()
    image = models.ImageField(upload_to="images/", default="images/default.webp")
    categories = models.ManyToManyField(Category)
    is_edible = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    countries = models.ManyToManyField(Country, related_name="plants", blank=True)
    def __str__(self):
        return self.name
    
class Comment(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="plant_comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return f"{self.name} on {self.plant.name}"