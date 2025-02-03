import React, { useState, useEffect } from "react";
import axios from "axios";


function VehiclesForm({ vehicles, setVehicles, fetchVehicles }) {

    const [formData, setFormData] = useState({
        name: "",
        consumption: "",
        autonomy: "",
        weight_capacity: "",
    }); // Estado para el formulario



    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post("http://127.0.0.1:8000/api/vehicles/", formData); // Asegúrate de que esta sea tu ruta correcta
            setVehicles([...vehicles, response.data]); // Actualiza la lista con el nuevo vehículo
            setFormData({
                name: "",
                consumption: "",
                autonomy: "",
                weight_capacity: "",
            }); // Limpia el formulario
        } catch (error) {
            console.error("Error al crear el vehículo:", error);
        } finally{
            fetchVehicles();
        }
    };
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };
    
    return (
        <div>
            <form onSubmit={handleSubmit} className="mt-5">
                    <div>
                        <label>Nombre:</label>
                        <input
                            type="text"
                            name="name"
                            value={formData.name}
                            onChange={handleChange}
                            required
                        />
                    </div>
                    <div>
                        <label>Consumo (L/100km):</label>
                        <input
                            type="number"
                            name="consumption"
                            value={formData.consumption}
                            onChange={handleChange}
                            required
                        />
                    </div>
                    <div>
                        <label>Autonomía (km):</label>
                        <input
                            type="number"
                            name="autonomy"
                            value={formData.autonomy}
                            onChange={handleChange}
                            required
                        />
                    </div>
                    <div>
                        <label>Capacidad de carga (kg):</label>
                        <input
                            type="number"
                            name="weight_capacity"
                            value={formData.weight_capacity}
                            onChange={handleChange}
                            required
                        />
                    </div>
                    <button type="submit" className="mt-3 bg-blue-500 text-white px-4 py-2">
                        Agregar Vehículo
                    </button>
                </form>
        </div>
    )
}

export default VehiclesForm;