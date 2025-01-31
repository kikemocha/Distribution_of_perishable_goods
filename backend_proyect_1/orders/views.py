from rest_framework import viewsets
from .models import Cliente, Order
from .serializers import ClienteSerializer, OrderSerializer

# CRUD para Clientes
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

# CRUD para Orders
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
