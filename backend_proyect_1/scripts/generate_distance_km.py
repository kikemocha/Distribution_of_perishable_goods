import requests
import pandas as pd
import numpy as np
import time
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

# 📌 Ruta absoluta del archivo df_location.csv
location_path = os.path.join(script_dir, "df_location.csv")

# 📌 Verificar si el archivo existe
if not os.path.exists(location_path):
    raise FileNotFoundError(f"❌ No se encontró el archivo: {location_path}")

# 📌 Cargar ubicaciones
df_locations = pd.read_csv(location_path)
# Lista de clientes con coordenadas
locations = df_locations[['Cliente', 'Latitud', 'Longitud']].values.tolist()

# Inicializar matrices de distancia y tiempo
distance_matrix = np.zeros((len(locations), len(locations)))
time_matrix = np.zeros((len(locations), len(locations)))

# Función para hacer una solicitud a OSRM
def get_route(osrm_url, origen, destino):
    url = f"{osrm_url}/route/v1/driving/{origen[2]},{origen[1]};{destino[2]},{destino[1]}?overview=false"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        distance = data['routes'][0]['distance'] / 1000  # Convertir a km
        duration = data['routes'][0]['duration'] / 60  # Convertir a minutos
        return distance, duration
    else:
        print(f"Error {response.status_code}: No se pudo obtener la ruta entre {origen[0]} y {destino[0]}")
        return None, None

# Iterar sobre las ubicaciones y calcular rutas
osrm_url = "http://router.project-osrm.org"
for i in range(len(locations)):
    for j in range(i + 1, len(locations)):  # Solo calcular la mitad superior
        distance, duration = get_route(osrm_url, locations[i], locations[j])
        
        if distance is not None and duration is not None:
            # Llenar matrices simétricas
            distance_matrix[i][j] = distance_matrix[j][i] = distance
            time_matrix[i][j] = time_matrix[j][i] = duration

        time.sleep(1)  # Evitar sobrecargar el servidor

# Crear DataFrames con los resultados
distance_df = pd.DataFrame(distance_matrix, columns=[l[0] for l in locations], index=[l[0] for l in locations])
time_df = pd.DataFrame(time_matrix, columns=[l[0] for l in locations], index=[l[0] for l in locations])

# Guardar los resultados en archivos Excel
distance_df.to_excel(f"{script_dir}/matriz_distancias.xlsx")
time_df.to_excel(f"{script_dir}/matriz_tiempos.xlsx")

