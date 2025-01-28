import React, { useState, useEffect } from "react";
import axios from "axios";
import VehiclesForm from "./VehiclesForm";

function AdminPage() {
    const [vehicles, setVehicles] = useState([]);

    // Función para obtener la lista de vehículos
    const fetchVehicles = async () => {
        try {
            const response = await axios.get("http://127.0.0.1:8000/api/vehicles/"); // Asegúrate de que esta sea tu ruta correcta
            setVehicles(response.data);
        } catch (error) {
            console.error("Error al obtener los vehículos:", error);
        }
    };
    useEffect(() => {
        fetchVehicles();
    }, []);

    return (
        <div>
            <div className="h-20 flex items-center justify-center sticky top-0 z-10 bg-neutral-100">
                <img src="https://www.mercadona.es/static/media/mercadona-logo.a65a34320ed4e902bf30.svg" alt="Mercadona Logo" />
            </div>
            <h3 className="w-full text-7xl text-center my-5">Almacén</h3>
            <iframe
                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d893.0174139397423!2d-3.727886252840567!3d40.388777877865465!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xd4227945c406263%3A0x5f73074fad962fc!2sMercadona!5e1!3m2!1ses!2ses!4v1733249317345!5m2!1ses!2ses"
                width="600"
                height="450"
                allowFullScreen=""
                loading="lazy"
                referrerPolicy="no-referrer-when-downgrade"
            ></iframe>
            <div className="border-t-2 mt-12">
                <h3 className="w-full text-5xl text-center my-5">Vehículos</h3>
                {/* Lista de vehículos */}
                <div className="grid grid-cols-4">
                    {vehicles.map((vehicle) => (
                        <div className="bg-green-100 hover:bg-green-300 m-2 border-slate-950 h-72 rounded-2xl">
                            <div className="flex justify-center mt-4">
                                    <img className="h-20 w-auto" src="mercadona_car.png" alt="" />
                            </div>
                            <div>
                                <h5 className="font-bold text-center mt-2">{vehicle.name}</h5>
                            </div>
                            <div className="mt-4 space-y-2 w-full">
                                <div className="flex items-center justify-center">
                                    <span className="mr-4">Consumo:</span>
                                    <span>{vehicle.consumption} L/100km</span>
                                </div>
                                <div className="flex items-center justify-center">
                                    <span className="mr-4">Autonomía:</span>
                                    <span>{vehicle.autonomy} km</span>
                                </div>
                                <div className="flex items-center justify-center">
                                    <span className="mr-4">Capacidad:</span>
                                    <span>{vehicle.weight_capacity} kg</span>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
                <VehiclesForm vehicles={vehicles} setVehicles={setVehicles} fetchVehicles={fetchVehicles}/>
            </div>
        
        </div>
    );
}

export default AdminPage;
