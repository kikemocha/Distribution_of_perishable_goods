// src/components/Home.js
import React, { useState, useEffect }     from 'react';
import { useCart } from '../Context/CartContext.tsx';
import { regions } from './regions.js';

function CartProducts({ show, onClose }) {
    
    const { state } = useCart();
    const [endOrder, setEndOrder] = useState(false);
    
    useEffect(() => {
        if (show) {
          document.body.style.overflow = 'hidden'; // Disable scroll
        } else {
          document.body.style.overflow = 'auto'; // Enable scroll
        }
        // Cleanup function to restore scroll when the component is unmounted or show changes
        return () => {
          document.body.style.overflow = 'auto';
        };
      }, [show]);

    if (!show) {
      return null;
    }

    const total = parseFloat(
        state.products.reduce((sum, product) => {
          const price = product.price_with_discount ?? product.real_price ?? 0;
          const quantity = product.userQuantity ?? 0;
          return sum + price * quantity;
        }, 0).toFixed(2)
      );


    return (
        <div 
          className="fixed inset-0 bg-gray-800 bg-opacity-50 z-40 flex items-center justify-center"
        >
          <div className="relative bg-white w-1/2 h-4/5 rounded-lg p-6">
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
            {endOrder ?(
                <div className='h-full w-full'>
                    <div 
                        onClick={(e) => {
                            e.stopPropagation(); // Detiene la propagación del evento click
                            setEndOrder(false);
                          }}
                        className='absolute z-50 cursor-pointer left-5 top-5 flex'
                        >
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 19.5 3 12m0 0 7.5-7.5M3 12h18" />
                        </svg>
                        <p className='ml-2'>Atrás</p>
                    </div>
                    <div className='h-1/3 w-full py-5 flex'>
                        <div className='h-full w-1/2 rounded-3xl bg-slate-200 m-5'>
                            <div className='h-1/2 w-full pb-4 flex items-end justify-center '>
                                <p className='text-4xl text-center '>TOTAL</p>  
                            </div>
                            <p className='h-1/2 w-full text-4xl text-center'>{total} €</p>
                        </div>

                        <div className='h-full w-1/2 p-5 rounded-3xl bg-slate-200 m-5'>
                        <div>
                          <label className="block text-sm font-medium text-gray-700">Nombre</label>
                          <input
                              type="text"
                              className="mt-1 block w-full p-2 border border-gray-300 rounded-lg focus:ring focus:ring-blue-400 focus:outline-none"
                          />
                          </div>
                          <div>
                          <label className="block text-sm font-medium text-gray-700">Apellidos</label>
                          <input
                              type="text"
                              className="mt-1 block w-full p-2 border border-gray-300 rounded-lg focus:ring focus:ring-blue-400 focus:outline-none"
                          />
                          </div>
                        </div>
                    </div>
                    <div className='h-2/3 w-full py-5 px-5 pb-20'>
                        <div className='bg-slate-200 p-5 w-full h-full rounded-3xl'>
                        <div className="h-full space-y-4 flex flex-col justify-around">
                          <div>
                          <label className="block text-sm font-medium text-gray-700">Calle</label>
                          <input
                              type="text"
                              className="mt-1 block w-full p-2 border border-gray-300 rounded-lg focus:ring focus:ring-blue-400 focus:outline-none"
                          />
                          </div>

                          <div className="grid grid-cols-3 gap-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Número</label>
                                <input
                                type="text"
                                className="mt-1 block w-full p-2 border border-gray-300 rounded-lg focus:ring focus:ring-blue-400 focus:outline-none"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Piso</label>
                                <input
                                type="text"
                                className="mt-1 block w-full p-2 border border-gray-300 rounded-lg focus:ring focus:ring-blue-400 focus:outline-none"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Puerta</label>
                                <input
                                type="text"
                                className="mt-1 block w-full p-2 border border-gray-300 rounded-lg focus:ring focus:ring-blue-400 focus:outline-none"
                                />
                            </div>
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">Código Postal</label>
                                    <input
                                    type="text"
                                    className="mt-1 block w-full p-2 border border-gray-300 rounded-lg focus:ring focus:ring-blue-400 focus:outline-none"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">Ciudad</label>
                                    <select
                                        name="location"
                                        className="w-full p-2 border rounded-lg bg-white text-black"
                                    >
                                    <option value="">Selecciona una ciudad</option>
                                    {regions.map((region) => (
                                        <optgroup key={region.name} label={region.name}>
                                        {region.provinces.map((province) => (
                                            <option key={province} value={province}>
                                            {province}
                                            </option>
                                        ))}
                                        </optgroup>
                                    ))}
                                    </select>
                                </div>
                            </div>
                          </div>
                        </div>
                    </div>
                    <div
                        onClick={(e) => {
                            e.stopPropagation(); // Detiene la propagación del evento click
                            onClose();
                          }}
                        className='cursor-pointer mb-4 h-12 w-1/2 right-1/4 bg-green-500 absolute bottom-0 rounded-full flex items-center justify-center'>
                            <p className='text-center cursor-pointer' >REALIZAR PEDIDO</p>
                    </div>
                </div>
            ):
            (
                <div className='h-full'>
                    <div className='h-full pb-12 overflow-y-scroll'>
                        {state.products.map(product => (
                            <div className='h-16 bg-slate-100 m-4 rounded-2xl p-2 flex'>
                            <img src={product.img} alt="" className='h-12' />
                            <p className="w-1/2 font-bold truncate flex items-center">{product.label}</p>
                            <div className='flex justify-center items-center w-1/4'>
                                <p>{product.userQuantity}</p>
                            </div>
                            <div className='flex justify-center items-center w-1/4'>
                            <p>
                                {
                                product.price_with_discount ? (    
                                    Math.round((product.price_with_discount * (product.userQuantity ?? 0))* 100 )/100
                                ) : product.real_price && (
                                    Math.round((product.real_price * (product.userQuantity ?? 0))* 100 )/100
                                )
                                }
                                €   
                            </p>
                            </div>
                            <div className='flex justify-center items-center text-red-600'>
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
                                <path strokeLinecap="round" strokeLinejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                                </svg>
                            </div>
                            </div>
                            ))
                            }
                            <div className='h-32 w-3/4 rounded-3xl mx-auto bg-slate-300 flex'>
                                <div className='w-1/2 flex items-center justify-center'>
                                    <p className='text-4xl font-bold text-center'>TOTAL: </p>
                                </div>
                                <div className='w-1/2 flex items-center justify-center'>
                                    <p className='text-4xl font-bold'>{total}€</p>
                                </div>
                            </div>
                    </div>
                    <div
                        onClick={(e) => {
                            e.stopPropagation(); // Detiene la propagación del evento click
                            setEndOrder(true);
                          }}
                        className='cursor-pointer mb-4 h-12 w-1/2 right-1/4 bg-yellow-300 absolute bottom-0 rounded-full flex items-center justify-center'>
                            <p className='text-center cursor-pointer' >FINALIZAR PEDIDO</p>
                    </div>
                </div>
            )}
            
            
          </div>
        </div>
      );
  }

export default CartProducts;
