// src/components/Home.js
import React, { useState }     from 'react';

function PopUpProducts({ show, product, onClose }) {
    const [productCount, setProductCount] = useState(1);

    if (!show) {
      return null;
    }
  
    return (
        <div 
          className="fixed inset-0 bg-gray-800 bg-opacity-50 z-40 flex items-center justify-center"
          onClick={onClose}
        >
          <div className="relative bg-white w-1/2 h-3/5 rounded-lg p-6" onClick={(e) => e.stopPropagation()}>
            <svg 
                xmlns="http://www.w3.org/2000/svg" 
                fill="none" 
                viewBox="0 0 24 24" 
                strokeWidth={1.5} 
                stroke="currentColor" 
                className="size-6 absolute z-50 cursor-pointer right-5 top-5"
                onClick={onClose}
                >
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18 18 6M6 6l12 12" />
            </svg>
            <div className='flex h-full'>
                <div className='w-1/2 h-full flex justify-center align-middle'>
                    <img src={product.img} alt={product.label} className="object-contain" />
                </div>
                <div className= 'w-full flex flex-col justify-between'>
                    <div>
                        <h3 className="text-xl font-bold mb-4 mt-12">{product.label}</h3>
                    
                        <p>Precio: <p className='font-bold text-xl text-red-500'>{product.price_with_discount || product.real_price}€ <span className='font-normal text-gray-500'>{product.quantity}</span></p></p>
                    </div>
                    <div>
                        <div className='h-16 bg-gray-300 w-2/5 flex rounded-full mx-auto mt-full'>
                            <div
                                className="border border-black rounded-s-full w-14 h-16 cursor-pointer text-7xl flex justify-center items-center hover:bg-gray-500"
                                onClick={() => {
                                    if (productCount > 0) setProductCount(productCount - 1);
                                }}
                                >
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    strokeWidth={2} // Puedes ajustar el grosor del borde aquí
                                    stroke="currentColor"
                                    className="w-6 h-6" // Ajusta el tamaño del icono
                                >
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M5 12h14" />
                                </svg>
                            </div>
                            <div className='mx-auto text-3xl my-auto'>{productCount}</div>
                            <div
                                className="border border-black rounded-e-full w-14 h-16 cursor-pointer text-7xl flex justify-center items-center hover:bg-gray-500"
                                onClick={() => {
                                    setProductCount(productCount + 1);
                                }}
                                >
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                                </svg>

                            </div>
                        </div>
                        <div className='flex justify-center mt-7'>
                            <button className='bg-[#fcb831] py-2 px-4 rounded-full h-20 w-56 font-semibold' >
                                AÑADIR AL CARRO
                            </button>
                        </div>
                    </div>
                </div>

            </div>
            
          </div>
        </div>
      );
  }

export default PopUpProducts;
