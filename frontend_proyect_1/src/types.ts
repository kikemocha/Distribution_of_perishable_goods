export interface Product {
    id: number;
    category : string;
    subcategory: string;
    img: string;
    label: string;
    sub_label: string;
    price_before_discount: number;
    price_with_discount: number;
    product_type: string;
    quantity: string;
    name: string;
    real_price: number;
    userQuantity?: number;
  }
