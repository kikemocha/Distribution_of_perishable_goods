# app1/management/commands/import_csv.py
import csv
import os
from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Importa datos desde un archivo CSV en la carpeta data'

    def add_arguments(self, parser):
        parser.add_argument('alimentos_mercadona.csv', type=str, help='Nombre del archivo CSV en la carpeta data')

    def handle(self, *args, **kwargs):
        csv_filename = kwargs['alimentos_mercadona.csv']
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_path = os.path.join(base_dir, '..', '..','data', csv_filename)

        try:
            with open(csv_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Limpiar y convertir los valores del CSV
                    price_with_discount = row.get('price_with_discount')
                    price_before_discount = row.get('price_before_discount')
                    real_price = row.get('real_price')

                    # Convertir precios a Decimal o None si están vacíos
                    price_with_discount = float(price_with_discount.replace(",", ".")) if price_with_discount else None
                    price_before_discount = float(price_before_discount.replace(",", ".")) if price_before_discount else None
                    real_price = float(real_price.replace(",", ".")) if real_price else None

                    # Crear el objeto Producto
                    Product.objects.create(
                        category=row.get('category'),
                        subcategory=row.get('subcategory'),
                        product_type=row.get('product_type'),
                        label=row.get('label'),
                        sub_label=row.get('sub_label'),
                        price_with_discount=price_with_discount,
                        price_before_discount=price_before_discount,
                        real_price=real_price,
                        quantity=row.get('quantity'),
                        img=row.get('img')
                    )

            self.stdout.write(self.style.SUCCESS(f'Datos importados correctamente desde {csv_filename}'))
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f'El archivo {csv_filename} no se encontró en la carpeta data'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error al importar datos: {e}'))