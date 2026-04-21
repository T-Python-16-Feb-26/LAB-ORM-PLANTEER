from django.db import models
 
 
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Plant(models.Model):
    name = models.CharField(max_length=200)
    scientific_name = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='plants', null=True, blank=True)
    image = models.ImageField(upload_to='plants/', blank=True, null=True)
    is_edible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return self.image.url
        return '/static/images/default-plant.png'

    def get_related_plants(self):
        return Plant.objects.filter(category=self.category).exclude(pk=self.pk)[:4]
    


class Review(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created']
    def __str__(self):
        return f"Review for {self.plant.name} - {self.rating} Stars"
