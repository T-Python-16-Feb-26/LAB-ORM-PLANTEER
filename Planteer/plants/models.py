from django.db import models
from django.contrib.auth.models import User


class Country(models.Model):
    name = models.CharField(max_length=100)
    flag = models.ImageField(upload_to='countries/', null=True, blank=True)

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Plant(models.Model):

    CATEGORIES = [
        ('Fruit', 'Fruit'),
        ('Vegetable', 'Vegetable'),
        ('Flower', 'Flower'),
        ('Tree', 'Tree'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='plants/images', blank=True, null=True)

    category = models.CharField(max_length=100, choices=CATEGORIES, default='Fruit')
    is_edible = models.BooleanField(default=False)

    countries = models.ManyToManyField(Country, related_name="plants")

 
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        related_name="plants",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Comment(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)