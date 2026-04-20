from django.db import models

# Create your models here.

class Plant(models.Model):

    class CategoryChoices(models.TextChoices):
        FLOWER = 'Flower', 'Flower'
        TREE = 'Tree', 'Tree'
        VEGETABLE = 'Vegetable', 'Vegetable'
        FRUIT = 'Fruit', 'Fruit'
        HERB = 'Herb', 'Herb'

    name_plant= models.CharField(max_length=1000)
    used_for=models.TextField()
    about= models.TextField()
    category = models.CharField(max_length=50, choices=CategoryChoices.choices)
    is_edible= models.BooleanField()
    created_at=models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='image/' , default="media/image/default.jpg")

class Comment(models.Model):

    plant=models.ForeignKey(Plant, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    comment=models.TextField()
    created_at_comment=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name} on {self.plant.name_plant}"