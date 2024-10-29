// src/components/Home.js
import React, { useState, useEffect } from 'react';
import Products from '../Components/Products';
import PopUpProducts from '../Components/ProductPopUp';

function Home() {
  const [showPopUpProduct, setShowPopUpProduct] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  const onClose = () => {
    setSelectedProduct(null);
    setShowPopUpProduct(false);
  };

  const handleProductClick = (product) => {
    setSelectedProduct(product);
    setShowPopUpProduct(true);
  };

  const fetchProducts = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/products/');
      const data = await response.json();
      setProducts(data);
    } catch (error) {
      console.error("Error fetching products:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  if (loading) return <p>Cargando productos...</p>;

  return (
    <div className="bg-neutral-100">
      <div className="h-20 flex items-center justify-center sticky top-0 z-10 bg-neutral-100">
        <img src="https://www.mercadona.es/static/media/mercadona-logo.a65a34320ed4e902bf30.svg" alt="Mercadona Logo" />
      </div>
      <div className="mx-24">
        <h1 className="font-bold text-xl h-10 pl-24">Productos</h1>
        <div className="grid grid-cols-5 gap-4 mt-5">
          {products.map((product) => (
            <Products
              key={product.id}
              product={product}
              onClick={() => handleProductClick(product)}
            />
          ))}
        </div>
      </div>
      {showPopUpProduct && (
        <PopUpProducts
          show={showPopUpProduct}
          product={selectedProduct}
          onClose={onClose}
        />
      )}
    </div>
  );
}

export default Home;
