from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=128,unique=True)
    flag = models.ImageField(upload_to='flags/',default='flags/default.jpg')

    def __str__(self):
        return self.name

class Plant(models.Model):

    class Category(models.TextChoices):
        FRUIT = 'FRUIT','Fruit'
        VEGETABLE = 'VEGETABLE','Vegetable'
        FLOWER = 'FLOWER','Flower'
        HERB = 'HERB','Herb'
        OTHER = 'OTHER','Other'
    name = models.CharField(max_length=100)
    about  = models.TextField()
    used_for = models.TextField()
    image = models.ImageField(upload_to='images/',default='images/default.jpg')
    category = models.CharField(max_length=20,choices=Category.choices,default=Category.OTHER)
    is_edible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    countries =models.ManyToManyField(Country)

    def __str__(self):
        return f"Plant: {self.name} - Category: {self.category}"


class Comment(models.Model):
    plant =models.ForeignKey(Plant,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"Comment by {self.name} on {self.plant.name}"
    