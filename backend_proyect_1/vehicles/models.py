from django.db import models

class Vehicle(models.Model):
    name = models.CharField(max_length=100, verbose_name="name")
    consumption = models.FloatField(verbose_name="consumption(litros/100km)")
    autonomy = models.FloatField(verbose_name="autonomy(km)")
    weight_capacity = models.FloatField(verbose_name="weight_capacity(kg)")

    def __str__(self):
        return self.name
