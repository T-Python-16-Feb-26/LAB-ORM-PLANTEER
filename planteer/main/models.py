from django.db import models

# that wasnt meant to be here oops
# class Plant(models.Model):
#     name = models.CharField(max_length=2048),
#     about = models.TextField(),
#     used_for = models.TextField(),
#     image = models.ImageField( upload_to=None, height_field=None, width_field=None, max_length=None),
#     is_edible = models.BooleanField(default= False),
#     created_at = models.DateTimeField(auto_now_add=True),

class Contact(models.Model):
    first_name = models.CharField(max_length=1024)
    last_name = models.CharField(max_length=1024)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.first_name + " " + self.last_name
    
