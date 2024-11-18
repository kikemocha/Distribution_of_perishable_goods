from django.db import models

# Create your models here.
class Product(models.Model):
    category = models.CharField(max_length=255)
    subcategory = models.CharField(max_length=255)
    product_type = models.CharField(max_length=255, blank=True, null=True)
    label = models.CharField(max_length=255)
    sub_label = models.CharField(max_length=255, blank=True, null=True)
    price_with_discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price_before_discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    real_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantity = models.CharField(max_length=50)  # Ej: "/ud.", puede ser un CharField si tiene texto específico
    img = models.URLField()

    def __str__(self):
        return f"{self.label} - {self.sub_label} ({self.category}/{self.subcategory})"