from rest_framework import generics, viewsets
from .models import Vehicle
from .serializers import VehicleSerializer

class VehicleListCreateAPIView(generics.ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

class VehicleRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

class VehicleViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar las operaciones CRUD del modelo Vehicle.
    """
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer