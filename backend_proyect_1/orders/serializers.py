from rest_framework import serializers
from .models import Cliente, Order

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    cliente = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all(), write_only=True)  # Acepta ID en POST
    cliente_name = serializers.CharField(source="cliente.name", read_only=True)  # Devuelve nombre en GET

    class Meta:
        model = Order
        fields = ['id', 'cliente', 'cliente_name', 'mes_anio', 'quantity_kg', 'created_at']
