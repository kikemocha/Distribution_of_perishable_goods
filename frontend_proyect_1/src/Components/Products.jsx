// src/components/Products.js
import React from 'react';

function Products({ product, onClick }) {
  return (
    <div
      onClick={onClick}
      className="bg-white rounded-2xl h-72 w-64 mb-5 shadow-lg pt-5 transition-transform duration-300 transform hover:scale-105 hover:cursor-pointer"
    >
      <div className="h-full flex flex-col justify-between">
        <img className="h-44 w-44 mx-auto" src={product.img} alt={product.label} />
        <h5 className="font-bold text-center px-5">{product.label}</h5>
        <div className="h-12 flex items-center justify-center">
          {product.price_before_discount ? (
            <div className="flex items-center space-x-3">
              <p className="line-through text-gray-500">{product.price_before_discount}€</p>
              <p className="font-bold text-xl text-red-500">{product.price_with_discount}€</p> <p className='text-gray-500'>{product.quantity}</p>
            </div>
          ) : (
            <p className="font-bold text-center">{product.real_price}€ <span className='text-gray-500 font-normal'>{product.quantity}</span></p>
          )}
        </div>
      </div>
    </div>
  );
}

export default Products;
