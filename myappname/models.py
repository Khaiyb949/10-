from django.db import models

# Create your models here.
class Image(models.Model):
    file = models.ImageField(upload_to='truyen_images/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.description
    
    