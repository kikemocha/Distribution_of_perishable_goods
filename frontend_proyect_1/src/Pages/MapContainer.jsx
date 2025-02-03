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

const ORS_API_KEY = "TU_API_KEY_AQUI"; // Reemplázala con tu clave de OpenRouteService

const generateRandomCoords = () => {
  const minLat = 40.35; // Sur de Madrid
  const maxLat = 40.55; // Norte de Madrid
  const minLon = -3.85; // Oeste de Madrid
  const maxLon = -3.55; // Este de Madrid

  const start = [
    (Math.random() * (maxLon - minLon)) + minLon,
    (Math.random() * (maxLat - minLat)) + minLat
  ];
  const end = [
    (Math.random() * (maxLon - minLon)) + minLon,
    (Math.random() * (maxLat - minLat)) + minLat
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
      setRouteCoords(route.map(coord => [coord[0], coord[1]])); // Mantiene el formato Lon, Lat
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
        const transformedCoords = routeCoords.map(coord => fromLonLat(coord));

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
      <button
        onClick={fetchRoute}
        className="absolute top-2 right-2 bg-blue-500 text-white px-4 py-2 rounded"
      >
        Nueva Ruta
      </button>
      <div ref={mapRef} className="w-full h-full" />
    </div>
  );
};

export default MapContainer;
