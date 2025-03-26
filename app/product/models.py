from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
class Product(models.Model):
    name = models.CharField(max_length=255)  # Product name
    description = models.TextField(blank=True)  # Optional description
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price (e.g., 19.99)
    stock = models.PositiveIntegerField(default=0)  # Number in stock
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of creation
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # References the active user model
        on_delete=models.CASCADE,  # Deletes products if the user is deleted
    )
    def __str__(self):
        return self.name
