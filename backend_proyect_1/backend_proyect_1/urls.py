from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products.views import ProductViewSet
from vehicles.views import VehicleViewSet
from orders.views import ClienteViewSet, OrderViewSet  # Importa Cliente y Order

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'vehicles', VehicleViewSet)
router.register(r'clientes', ClienteViewSet)  # Ruta para clientes
router.register(r'orders', OrderViewSet)  # Ruta para órdenes

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Incluye el enrutador de DRF
]
