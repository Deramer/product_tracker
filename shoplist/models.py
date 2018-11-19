from django.db import models

# Create your models here.

class ShoplistModel(models.Model):
    email = models.TextField()
    item = models.TextField()
