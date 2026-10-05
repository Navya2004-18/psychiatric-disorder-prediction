from django.db import models

# Create your models here.
class Disorders(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=255)
    password = models.CharField(max_length=55)
    contact = models.IntegerField()
    address = models.TextField(max_length=255)

    def __str__(self):
        return self.name
    

    