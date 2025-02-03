from django.db import models

class Cliente(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name

class Order(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="orders")
    quantity_kg = models.FloatField()
    mes_anio = models.CharField(max_length=7)  # Formato "MM-YYYY"
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Orden de {self.quantity_kg} kg para {self.cliente.name} en {self.mes_anio}"