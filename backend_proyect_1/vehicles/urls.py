from django.urls import path
from .views import VehicleListCreateAPIView, VehicleRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', VehicleListCreateAPIView.as_view(), name='vehicle_list_create'),
    path('<int:pk>/', VehicleRetrieveUpdateDestroyAPIView.as_view(), name='vehicle_detail_update_delete'),
]
