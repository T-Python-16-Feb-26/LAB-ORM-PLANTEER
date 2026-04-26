from django.db import models

# Create your models here.

class Plant(models.Model):

    CATEGORY_CHOICES = [
        ('indoor', 'Indoor'),
        ('outdoor', 'Outdoor'),
        ('flower', 'Flower'),
    ]

    LIGHT_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
 
    CARE_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    USED_FOR_CHOICES = [
        ('decorative', 'Decorative'),
        ('air_purifying', 'Air Purifying'),
        ('edible', 'Edible'),
    ]

    name = models.CharField(max_length=255)
    about = models.TextField()
    used_for = models.CharField(max_length=50, choices=USED_FOR_CHOICES)

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    light = models.CharField(max_length=20, choices=LIGHT_CHOICES)
    
    care_level = models.CharField(max_length=20, choices=CARE_CHOICES)

    image = models.ImageField(upload_to='plants/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.category})"

    class Meta:
        ordering = ['-created_at']