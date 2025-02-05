import React, { useRef, useEffect, useState } from "react";
import "ol/ol.css";
import { Map, View } from "ol";
import { fromLonLat } from "ol/proj";
import TileLayer from "ol/layer/Tile";
import { OSM } from "ol/source";
import VectorLayer from "ol/layer/Vector";
import VectorSource from "ol/source/Vector";
import { LineString } from "ol/geom";
import Feature from "ol/Feature";
import Stroke from "ol/style/Stroke";
import Style from "ol/style/Style";
import axios from "axios";

const ORS_API_KEY = "5b3ce3597851110001cf6248228c2c8d82c74e7d8a4186da6489a320"; // Reemplaza con tu clave de OpenRouteService

const generateRandomCoords = () => {
  const minLat = 40.35;
  const maxLat = 40.55;
  const minLon = -3.85;
  const maxLon = -3.55;

  const start = [
    Math.random() * (maxLon - minLon) + minLon,
    Math.random() * (maxLat - minLat) + minLat,
  ];
  const end = [
    Math.random() * (maxLon - minLon) + minLon,
    Math.random() * (maxLat - minLat) + minLat,
  ];

  return [start, end];
};

const MapContainer = () => {
  const mapRef = useRef(null);
  const mapInstanceRef = useRef(null);
  const [routeCoords, setRouteCoords] = useState([]);

  const fetchRoute = async () => {
    const coords = generateRandomCoords();
    const url = `https://api.openrouteservice.org/v2/directions/driving-car?api_key=${ORS_API_KEY}&start=${coords[0][0]},${coords[0][1]}&end=${coords[1][0]},${coords[1][1]}`;
    
    try {
      const response = await axios.get(url);
      const route = response.data.features[0].geometry.coordinates;
      setRouteCoords(route.map(coord => [coord[0], coord[1]]));
    } catch (error) {
      console.error("Error al obtener la ruta:", error);
    }
  };

  useEffect(() => {
    if (mapRef.current) {
      const tileLayer = new TileLayer({
        source: new OSM(),
      });

      if (!mapInstanceRef.current) {
        mapInstanceRef.current = new Map({
          target: mapRef.current,
          layers: [tileLayer],
          view: new View({
            center: fromLonLat([-3.7038, 40.4168]), // Centro en Madrid
            zoom: 12,
          }),
        });
      }

      if (routeCoords.length > 1) {
        const transformedCoords = routeCoords.map((coord) => fromLonLat(coord));

        const routeFeature = new Feature({
          geometry: new LineString(transformedCoords),
        });

        routeFeature.setStyle(
          new Style({
            stroke: new Stroke({
              color: "#ff0000",
              width: 3,
            }),
          })
        );

        const routeLayer = new VectorLayer({
          source: new VectorSource({
            features: [routeFeature],
          }),
        });

        mapInstanceRef.current.addLayer(routeLayer);
      }
    }
  }, [routeCoords]);

  return (
    <div className="w-full h-full relative">
      {/* Contenedor del botón para asegurarse de que se muestra correctamente */}
      <div className="absolute top-4 right-4 z-10">
        <button
          onClick={fetchRoute}
          className="bg-blue-600 hover:bg-blue-700 text-white font-bold px-4 py-2 rounded-lg shadow-md transition duration-300">
          Nueva Ruta
        </button>
      </div>

      {/* Mapa */}
      <div ref={mapRef} className="w-full h-full" />
    </div>
  );
};

export default MapContainer;
