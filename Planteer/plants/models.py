from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#main app

class Country (models.Model):
    
    name= models.CharField(max_length=512 ,unique=True)
    flag= models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Plant (models.Model):

    class Category (models.TextChoices):
        TREE = 'tree' , 'Tree'
        FRUIT = 'fruit' , 'Fruit'
        VEGETABLE = 'vegetable' , 'Vegetable'
        FLOWER = 'flower' , 'Flower'
        HERB = 'herb' , 'Herb'




    name = models.CharField(max_length=1024)
    about = models.TextField()
    used_for = models.TextField()
    image = models.ImageField(upload_to="images/")
    category= models.CharField(max_length=500,choices=Category.choices)
    is_edible = models.BooleanField(default=True)
    countries = models.ManyToManyField(Country)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment (models.Model):
    plant= models.ForeignKey(Plant,on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)