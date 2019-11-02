from django.db import models

# Create your models here.
class users(models.Model):
    name = models.TextField()
    age = models.PositiveSmallIntegerField()
    email = models.EmailField(max_length=254)
    contact = models.BigIntegerField()
