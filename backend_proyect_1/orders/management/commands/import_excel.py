import os
import pandas as pd
from pathlib import Path
from django.core.management.base import BaseCommand
from orders.models import Cliente, Order

class Command(BaseCommand):
    help = "Importar datos desde dos archivos Excel en Django ORM"

    def add_arguments(self, parser):
        parser.add_argument('df_orders.xlsx', type=str, help="Ruta del archivo Excel de órdenes")
        parser.add_argument('df_location.xlsx', type=str, help="Ruta del archivo Excel de ubicaciones")

    def handle(self, *args, **kwargs):
        archivo_orders = kwargs['df_orders.xlsx']
        archivo_clients = kwargs['df_location.xlsx']

        # Obtener la ruta base del proyecto
        base_dir = Path(__file__).resolve().parent.parent.parent.parent  
        excel_path_orders = base_dir / 'data' / archivo_orders
        excel_path_clients = base_dir / 'data' / archivo_clients

        # Verificar si los archivos existen
        if not excel_path_orders.exists():
            self.stderr.write(self.style.ERROR(f"El archivo {excel_path_orders} no existe."))
            return
        
        if not excel_path_clients.exists():
            self.stderr.write(self.style.ERROR(f"El archivo {excel_path_clients} no existe."))
            return

        self.importar_excel_clients(excel_path_clients)
        self.importar_excel_orders(excel_path_orders)

    def importar_excel_clients(self, archivo):
        """Importar datos desde Excel (df_location.xlsx)"""
        df_clients = pd.read_excel(archivo, engine='openpyxl')
        for _, row in df_clients.iterrows():
            cliente, created = Cliente.objects.get_or_create(
                name=row['cliente'],
                defaults={
                    'latitude': row['Latitud'],
                    'longitude': row['Longitud']
                }
            )
        self.stdout.write(self.style.SUCCESS(f'Datos de ubicaciones importados correctamente desde {archivo}'))

    def importar_excel_orders(self, archivo):
        """Importar datos desde Excel (df_orders.xlsx)"""
        df_orders = pd.read_excel(archivo, engine='openpyxl')
        for _, row in df_orders.iterrows():
            try:
                cliente = Cliente.objects.get(name=row['cliente'])
                Order.objects.create(
                    cliente=cliente,
                    quantity_kg=row['order_demand'],
                    mes_anio=row.get('mes_anio', '01-2024')
                )
            except Cliente.DoesNotExist:
                self.stderr.write(self.style.ERROR(f"Cliente {row['cliente']} no encontrado en la base de datos."))
        self.stdout.write(self.style.SUCCESS(f'Datos de órdenes importados correctamente desde {archivo}'))

