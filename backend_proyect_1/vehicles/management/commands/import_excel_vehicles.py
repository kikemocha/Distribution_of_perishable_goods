import os
import pandas as pd
from pathlib import Path
from django.core.management.base import BaseCommand
from vehicles.models import Vehicle

class Command(BaseCommand):
    help = "Importar datos desde un archivo Excel de vehículos en Django ORM"

    def add_arguments(self, parser):
        parser.add_argument('df_vehicle.xlsx', type=str, help="Ruta del archivo Excel de vehículos")

    def handle(self, *args, **kwargs):
        archivo_vehicles = kwargs['df_vehicle.xlsx']

        # Obtener la ruta base del proyecto
        base_dir = Path(__file__).resolve().parent.parent.parent.parent  
        excel_path_vehicles = base_dir / 'data' / archivo_vehicles

        # Verificar si el archivo existe
        if not excel_path_vehicles.exists():
            self.stderr.write(self.style.ERROR(f"El archivo {excel_path_vehicles} no existe."))
            return

        self.importar_excel_vehicles(excel_path_vehicles)

    def importar_excel_vehicles(self, archivo):
        """Importar datos desde Excel (df_vehicle.xlsx)"""
        df_vehicles = pd.read_excel(archivo, engine='openpyxl')
        for _, row in df_vehicles.iterrows():
            Vehicle.objects.create(
                id=row['vehiculo_id'],
                name=row.get('name', f"Vehículo-{row['vehiculo_id']}"),
                weight_capacity=row['capacidad_kg'],
                consumption=row['costo_km'],
                autonomy=row['autonomia_km']
            )
        self.stdout.write(self.style.SUCCESS(f'Datos de vehículos importados correctamente desde {archivo}'))
