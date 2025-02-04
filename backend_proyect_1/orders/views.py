from rest_framework import viewsets
from .models import Cliente, Order
from .serializers import ClienteSerializer, OrderSerializer

import pandas as pd
import subprocess
import os
from django.http import JsonResponse
from django.db import connection  # Para ejecutar queries SQL directamente
from rest_framework.decorators import api_view
import json

# CRUD para Clientes
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

# CRUD para Orders
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

@api_view(["GET"])
def export_data_and_run_script(request):
    try:
        # 1️⃣ Ejecutar la consulta SQL para obtener órdenes
        query = """
            SELECT oc.name AS cliente, oo.quantity_kg AS order_demand
            FROM orders_order AS oo
            JOIN orders_cliente AS oc ON oo.cliente_id = oc.id;
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        
        # Directorio donde se guardarán los CSV (por ejemplo, ../scripts)
        script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts"))
        
        # 2️⃣ Guardar df_order.csv
        csv_path = os.path.join(script_dir, "df_order.csv")
        df.to_csv(csv_path, index=False)
        
        # 3️⃣ Consulta para obtener la ubicación de los clientes (df_location)
        query_2 = """
            SELECT name AS Cliente, latitude AS Latitud, longitude AS Longitud
            FROM orders_cliente;
        """
        with connection.cursor() as cursor:
            cursor.execute(query_2)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
        df_2 = pd.DataFrame(rows, columns=columns)
        csv_path = os.path.join(script_dir, "df_location.csv")
        df_2.to_csv(csv_path, index=False)
        
        # 4️⃣ Consulta para obtener los vehículos (df_vehicle)
        query_3 = """
            SELECT id AS vehiculo_id, weight_capacity AS capacidad_kg, 
                   consumption AS costo_km, autonomy AS autonomia_km, name
            FROM vehicles_vehicle;
        """
        with connection.cursor() as cursor:
            cursor.execute(query_3)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
        df_3 = pd.DataFrame(rows, columns=columns)
        csv_path = os.path.join(script_dir, "df_vehicle.csv")
        df_3.to_csv(csv_path, index=False)
        
        # 5️⃣ Llamar a main.py (que se encargará de ejecutar los algoritmos y devolver un JSON)
        script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts"))
        result = subprocess.run(["python3", os.path.join(script_dir, "main.py")],
                                capture_output=True, text=True)
        
        # Extraer la parte JSON (buscar la primera llave)
        json_start = result.stdout.find("{")
        if json_start == -1:
            return JsonResponse({"status": "error", "message": "No se encontró salida JSON."})
        json_str = result.stdout[json_start:]
        output_json = json.loads(json_str)
        return JsonResponse(output_json, json_dumps_params={'ensure_ascii': False})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})
