import React, { useState, useEffect } from "react";
import axios from "axios";

function AdminPage() {
    const [vehicles, setVehicles] = useState([]);
    const [clientes, setClientes] = useState([]);
    const [order, setOrder] = useState([]);
    
    const [showAddPopup, setShowAddPopup] = useState(false);
    const [showEditPopup, setShowEditPopup] = useState(false);
    const [selectedVehicle, setSelectedVehicle] = useState(null);
    const [formData, setFormData] = useState({ name: "", consumption: "", autonomy: "", weight_capacity: "" });

    const fetchVehicles = async () => {
        try {
            const response = await axios.get("http://127.0.0.1:8000/api/vehicles/");
            setVehicles(response.data);
        } catch (error) {
            console.error("Error al obtener los vehículos:", error);
        }
    };

    const fetchClients = async () => {
        try {
            const response = await axios.get("http://127.0.0.1:8000/api/clientes/");
            setClientes(response.data);
        } catch (error) {
            console.error("Error al obtener los clientes:", error);
        }
    };

    const fetchOrders = async () => {
        try {
            const response = await axios.get("http://127.0.0.1:8000/api/orders/");
            setOrder(response.data);
        } catch (error) {
            console.error("Error al obtener los orders:", error);
        }
    };
    useEffect(() => {
        fetchVehicles();
        fetchClients();
        fetchOrders();
    }, []);
    
    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const addVehicle = async () => {
        try {
            await axios.post("http://127.0.0.1:8000/api/vehicles/", formData);
            fetchVehicles();
            setShowAddPopup(false);
        } catch (error) {
            console.error("Error al añadir vehículo:", error);
        }
    };

    const editVehicle = async () => {
        try {
            await axios.put(`http://127.0.0.1:8000/api/vehicles/${selectedVehicle.id}/`, formData);
            fetchVehicles();
            setShowEditPopup(false);
        } catch (error) {
            console.error("Error al actualizar el vehículo:", error);
        }
    };

    const deleteVehicle = async (id) => {
        try {
            await axios.delete(`http://127.0.0.1:8000/api/vehicles/${id}/`);
            setVehicles(vehicles.filter(vehicle => vehicle.id !== id));
        } catch (error) {
            console.error("Error al eliminar el vehículo:", error);
        }
    };

    return (
        <div>
            <div className="h-20 flex items-center justify-center sticky top-0 z-10 bg-neutral-100">
                <img src="https://www.mercadona.es/static/media/mercadona-logo.a65a34320ed4e902bf30.svg" alt="Mercadona Logo" />
            </div>
            <h3 className="w-full text-7xl text-center my-5">Almacén</h3>
            <div className="border-t-2 mt-12">
                <h3 className="w-full text-5xl text-center my-5">Vehículos</h3>
                <button onClick={() => setShowAddPopup(true)} className="bg-green-600 hover:bg-green-800 text-white px-4 py-2 rounded-lg block mx-auto">+</button>
                <div className="grid grid-cols-4 px-96 mt-4">
                    {vehicles.map((vehicle) => (
                        <div key={vehicle.id} className="relative bg-green-100 hover:bg-green-300 m-2 border-slate-950 h-72 rounded-2xl p-4">
                            <button onClick={() => deleteVehicle(vehicle.id)} className="absolute top-2 right-2 bg-red-500 text-white px-2 py-1 rounded">X</button>
                            <div className="flex justify-center mt-4">
                                <img className="h-20 w-auto" src="mercadona_car.png" alt="" />
                            </div>
                            <h5 className="font-bold text-center mt-2">{vehicle.name}</h5>
                            <div className="mt-4 space-y-2 w-full">
                                <p>Consumo: {vehicle.consumption} L/100km</p>
                                <p>Autonomía: {vehicle.autonomy} km</p>
                                <p>Capacidad: {vehicle.weight_capacity} kg</p>
                            </div>
                            <button onClick={() => { setSelectedVehicle(vehicle); setFormData(vehicle); setShowEditPopup(true); }} className="bg-blue-500 text-white px-3 py-1 rounded-lg block mx-auto mt-2">Editar</button>
                        </div>
                    ))}
                </div>
            </div>

            <div className="border-t-2 mt-12">
                <h3 className="w-full text-5xl text-center my-5">Clientes</h3>
                <div className="">
                    <ul className="px-96">
                    {clientes.map((cliente) => (
                        <li className="bg-gray-400 m-2 h-12 flex rounded-lg">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-12">
                                <path strokeLinecap="round" strokeLinejoin="round" d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                            </svg>
                            <h5 className="font-bold text-center mt-2">{cliente.name}</h5>
                            <div className="h-36 mt-2 w-full flex justify-around ">
                                <p>Latitud: {cliente.latitude}</p>
                                <p>Longitud: {cliente.longitude}</p>
                            </div>
                        </li>
                    ))}

                    </ul>
                </div>
            </div>
            <div className="border-t-2 mt-12">
                <h3 className="w-full text-5xl text-center my-5">Orders</h3>
                <div className="">
                    <ul className="px-96 grid grid-cols-3">
                    {order.map((order) => (
                        <li key={order.id} className="bg-green-200 m-2 h-12 flex rounded-lg">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-12">
                                <path strokeLinecap="round" strokeLinejoin="round" d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                            </svg>
                            <h5 className="font-bold text-center mt-2">{order.cliente_name}</h5>
                            <div className="h-36 mt-2 w-full flex justify-around ">
                                <p>{order.mes_anio}</p>
                                <p>{order.quantity_kg} kg</p>
                            </div>
                        </li>
                    ))}

                    </ul>
                </div>
            </div>

            {/* Popup Añadir Vehículo */}
            {showAddPopup && (
                <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
                    <div className="bg-white p-6 rounded-lg">
                        <h2 className="text-lg font-bold">Añadir Vehículo</h2>
                        <input type="text" name="name" placeholder="Matrícula" onChange={handleChange} className="block border p-2 my-2 w-full" />
                        <input type="number" name="consumption" placeholder="Consumo" onChange={handleChange} className="block border p-2 my-2 w-full" />
                        <input type="number" name="autonomy" placeholder="Autonomía" onChange={handleChange} className="block border p-2 my-2 w-full" />
                        <input type="number" name="weight_capacity" placeholder="Capacidad" onChange={handleChange} className="block border p-2 my-2 w-full" />
                        <button onClick={addVehicle} className="bg-green-500 text-white px-4 py-2 rounded">Añadir</button>
                        <button onClick={() => setShowAddPopup(false)} className="bg-gray-500 text-white px-4 py-2 rounded ml-2">Cancelar</button>
                    </div>
                </div>
            )}

            {/* Popup Editar Vehículo */}
            {showEditPopup && (
                <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
                    <div className="bg-white p-6 rounded-lg">
                        <h2 className="text-lg font-bold">Editar Vehículo</h2>
                        <input type="text" name="name" value={formData.name} onChange={handleChange} className="block border p-2 my-2 w-full" />
                        <input type="number" name="consumption" value={formData.consumption} onChange={handleChange} className="block border p-2 my-2 w-full" />
                        <input type="number" name="autonomy" value={formData.autonomy} onChange={handleChange} className="block border p-2 my-2 w-full" />
                        <input type="number" name="weight_capacity" value={formData.weight_capacity} onChange={handleChange} className="block border p-2 my-2 w-full" />
                        <button onClick={editVehicle} className="bg-blue-500 text-white px-4 py-2 rounded">Guardar</button>
                        <button onClick={() => setShowEditPopup(false)} className="bg-gray-500 text-white px-4 py-2 rounded ml-2">Cancelar</button>
                    </div>
                </div>
            )}
        </div>
    );
}

export default AdminPage;
