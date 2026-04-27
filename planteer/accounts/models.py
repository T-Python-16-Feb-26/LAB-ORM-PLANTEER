from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='images/avatars/',default="images/avatars/default.png", blank=True)
    #TODO: make a fav list of plants
    
    def __str__(self) -> str:
        return f"Profile {self.user.username}"