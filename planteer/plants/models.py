from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)
    flag = models.ImageField( upload_to='countries/', height_field=None, width_field=None, max_length=None)
    def __str__(self) -> str:
        return self.name


class Plant(models.Model):
    class Category(models.TextChoices):
        TREE = 'tree', 'Tree'
        FRUIT = 'fruit', 'Fruit'
        VEGETABLE = 'vegetable', 'Vegetable'
        FLOWER = 'flower', 'Flower'
        HERB = 'herb', 'Herb'

    name = models.CharField(max_length=255)
    about = models.TextField()
    used_for = models.TextField()
    image = models.ImageField(upload_to='plants/')
    category = models.CharField(max_length=50, choices=Category.choices)
    is_edible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    countries = models.ManyToManyField(Country )
    def __str__(self) -> str:
        return self.name

class Comments(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=255)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return (self.name + self.user.username)
    
#TODO: make a class for  countries andlink it up with the plants in many to many relation,
#also add an  admin panel to add countries
#make sure to update the html to offer a dropdown to chose the countries
