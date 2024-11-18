from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()  # Consulta para obtener todos los productos
    serializer_class = ProductSerializer 