from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=255)
    flag = models.URLField()

    def __str__(self):
        return self.name


class Plant(models.Model):
    class Category(models.TextChoices):
        HERB = "Herb", "Herb"
        FLOWER = "Flower", "Flower"
        TREE = "Tree", "Tree"
        VEGETABLE = "Vegetable", "Vegetable"
        FRUIT = "Fruit", "Fruit"

    name = models.CharField(max_length=255)
    about = models.TextField()
    used_for = models.TextField()
    image = models.URLField()
    category = models.CharField(max_length=50, choices=Category.choices)
    is_edible = models.BooleanField(default=False)
    countries = models.ManyToManyField(Country, related_name='plants')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.plant.name}"