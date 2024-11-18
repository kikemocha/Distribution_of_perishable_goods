import csv
import os
from products.models import Product

def load_data_from_csv():
    file_path = os.path.join(os.path.dirname(__file__), '../../alimentos_mercadona.csv')
    with open(file_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            Product.objects.create(
                category=row['category'],
                subcategory=row['subcategory'],
                product_type=row.get('product_type'),
                label=row['label'],
                sub_label=row.get('sub_label'),
                price_with_discount=float(row['price_with_discount'].replace(",", ".")) if row['price_with_discount'] else None,
                price_before_discount=float(row['price_before_discount'].replace(",", ".")) if row['price_before_discount'] else None,
                real_price=float(row['real_price'].replace(",", ".")) if row['real_price'] else None,
                quantity=row['quantity'],
                img=row['img']
            )
