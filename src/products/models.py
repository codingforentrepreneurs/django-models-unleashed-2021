from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=None)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)