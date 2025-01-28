from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products.views import ProductViewSet
from vehicles.views import VehicleViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)  # Ruta para productos
router.register(r'vehicles', VehicleViewSet)  # Ruta para vehículos


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Incluye el enrutador de DRF
]
    