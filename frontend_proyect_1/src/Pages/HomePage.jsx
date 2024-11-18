// src/components/Home.js
import React, { useState, useEffect } from 'react';
import Products from '../Components/Products';
import PopUpProducts from '../Components/ProductPopUp.tsx';
import { useCart } from '../Context/CartContext.tsx';
import CartProducts from '../Components/cartProducts.tsx';

function Home() {
  const [showPopUpProduct, setShowPopUpProduct] = useState(false);
  const [showCart, setShowCart] = useState(false);

  const [showCartProduct, setShowCartProduct] = useState(true);
  
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  const { state } = useCart();

  const onClose = () => {
    setSelectedProduct(null);
    setShowPopUpProduct(false);
    setShowCartProduct(false);
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
        <div className='absolute flex justify-center items-center h-full w-24 right-4'>
          {state.products.length > 0 && (
            <div className='absolute flex justify-center items-center bg-red-500 h-5 w-5 right-4 top-2 rounded-full'>
            <p className='text-sm'>{state.products.length}</p>
          </div>
          )}
          <svg
            onClick={()=>{setShowCart(true)}} 
            xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="cursor-pointer size-12 m-2 p-3 bg-gray-400 rounded-2xl">
            <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 0 0-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 0 0-16.536-1.84M7.5 14.25 5.106 5.272M6 20.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm12.75 0a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z" />
          </svg>
        </div>
        {showCart && (
                  <div className='absolute rounded-3xl mt-4 bg-white h-96 w-1/4 right-12 top-16 border-2 border-black'>
                  <svg 
                    xmlns="http://www.w3.org/2000/svg" 
                    fill="none" 
                    viewBox="0 0 24 24" 
                    strokeWidth={1.5} 
                    stroke="currentColor" 
                    className="size-6 absolute z-50 cursor-pointer right-5 top-5"
                    onClick={() => setShowCart(false)}
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" d="M6 18 18 6M6 6l12 12" />
                  </svg>
                
                  {/* Contenedor del contenido del carrito con scroll */}
                  <div className='overflow-y-scroll h-80 py-12'>
                    {state.products.map(product => (
                      <div className='h-16 bg-white m-4 rounded-2xl p-2 flex'>
                        <img src={product.img} alt="" className='h-12' />
                        <p className="w-1/2 font-bold truncate flex items-center">{product.label}</p>
                        <div className='flex justify-center items-center w-1/4'>
                          <p>{product.userQuantity}</p>
                        </div>
                        <div className='flex justify-center items-center text-red-600'>
                          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
                            <path strokeLinecap="round" strokeLinejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                          </svg>
                        </div>
                      </div>
                    ))}
                  </div>
                
                  {/* Botón fijo en la parte inferior */}
                  <div className='h-12 w-1/2 right-1/4 bg-yellow-300 absolute bottom-0 rounded-full flex items-center justify-center'>
                    <p className='text-center cursor-pointer' onClick={()=>{setShowCartProduct(true); setShowCart(false)}}>FINALIZAR PEDIDO</p>
                  </div>
                </div>
                
        )}
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
      {showCartProduct && (
        <CartProducts
        show={showCartProduct}
        onClose={onClose}
        />
      )}
    </div>
  );
}

export default Home;
