import numpy as np
import pandas as pd
import random
# Cargar datasets
df_orders = pd.read_csv('df_order.csv')
df_vehicle = pd.read_excel('df_vehicle.xlsx')
df_distance_km = pd.read_excel('df_distance_km.xlsx')



# Configuración inicial
SEED = 10
np.random.seed(SEED)
random.seed(SEED)

# Variables de entrada
clientes = [f"cliente_{i+1}" for i in range(len(df_orders))]
vehiculos = list(df_vehicle["vehiculo_id"])

# Diccionarios clave
demanda = dict(zip(clientes, df_orders["order_demand"]))
capacidad_vehiculo = dict(zip(df_vehicle["vehiculo_id"], df_vehicle["capacidad_kg"]))
coste_km = dict(zip(df_vehicle["vehiculo_id"], df_vehicle["costo_km"]))
autonomia = dict(zip(df_vehicle["vehiculo_id"], df_vehicle["autonomia_km"]))
nombre_almacen = "Almacén"

# Añadir el almacén a la matriz de distancias
clientes_y_almacen = clientes + [nombre_almacen]
df_distance_km.index = clientes_y_almacen
df_distance_km.columns = clientes_y_almacen
dicc_distancia = df_distance_km.to_dict()

# Función para calcular la distancia total de una ruta
def calcular_distancia(ruta):
    distancia = 0
    for i in range(len(ruta) - 1):
        if dicc_distancia[ruta[i]][ruta[i + 1]] == 0:
            return float("inf")  # Ruta imposible
        distancia += dicc_distancia[ruta[i]][ruta[i + 1]]
    return distancia

# Función para calcular la carga total de una ruta
def calcular_carga(ruta):
    return sum(demanda.get(cliente, 0) for cliente in ruta)

# Función para validar un lote de clientes
def validar_lote(lote):
    for i in range(len(lote) - 1):
        if dicc_distancia[lote[i]][lote[i + 1]] == 0:
            return False  # Conexión imposible
    return True

# Función para dividir clientes en lotes válidos para un vehículo
def dividir_clientes(clientes_pendientes, capacidad, autonomia):
    lotes = []
    clientes_actuales = clientes_pendientes.copy()
    while clientes_actuales:
        lote = []
        carga_actual = 0
        distancia_actual = 0
        for cliente in clientes_actuales:
            if demanda[cliente] + carga_actual <= capacidad:
                carga_actual += demanda[cliente]
                lote.append(cliente)
                if len(lote) > 1:
                    distancia_actual += dicc_distancia[lote[-2]][lote[-1]]
                if distancia_actual > autonomia:
                    lote.pop()
                    break
        if lote and validar_lote(lote):
            for cliente in lote:
                clientes_actuales.remove(cliente)
            lotes.append(lote)
        else:
            break
    return lotes

# Función para optimizar una ruta para un lote de clientes y un vehículo
def optimizar_ruta_lote(lote, vehiculo):
    mejor_ruta = None
    mejor_costo = float("inf")

    # Ruta inicial aleatoria
    ruta_actual = [nombre_almacen] + random.sample(lote, len(lote)) + [nombre_almacen]
    coste_actual = calcular_distancia(ruta_actual) * coste_km[vehiculo]

    # Optimización local con Hill Climbing
    while True:
        vecinos = obtener_vecinos(ruta_actual)
        siguiente_ruta = None
        siguiente_costo = float("inf")

        for vecino in vecinos:
            distancia = calcular_distancia(vecino)
            if distancia <= autonomia[vehiculo] and distancia != float("inf"):
                coste_vecino = distancia * coste_km[vehiculo]
                if coste_vecino < siguiente_costo:
                    siguiente_ruta = vecino
                    siguiente_costo = coste_vecino

        if siguiente_costo >= coste_actual:
            break

        ruta_actual, coste_actual = siguiente_ruta, siguiente_costo

    mejor_ruta = ruta_actual
    mejor_costo = coste_actual
    return mejor_ruta, mejor_costo

# Función para generar rutas vecinas
def obtener_vecinos(ruta):
    vecinos = []
    for i in range(1, len(ruta) - 2):  # No intercambiamos el almacén
        for j in range(i + 1, len(ruta) - 1):
            vecino = ruta.copy()
            vecino[i], vecino[j] = vecino[j], vecino[i]
            if calcular_distancia(vecino) != float("inf"):  # Validar ruta
                vecinos.append(vecino)
    return vecinos

# Función para distribuir dinámicamente clientes entre vehículos
def distribuir_rutas_cooperativa():
    clientes_pendientes = clientes.copy()
    rutas_totales = []
    coste_total = 0

    while clientes_pendientes:
        mejor_ruta = None
        mejor_costo = float("inf")
        mejor_vehiculo = None

        for v in vehiculos:
            lotes = dividir_clientes(clientes_pendientes, capacidad_vehiculo[v], autonomia[v])
            for lote in lotes:
                if not validar_lote(lote):
                    continue
                ruta, coste = optimizar_ruta_lote(lote, v)
                if coste < mejor_costo:
                    mejor_ruta = ruta
                    mejor_costo = coste
                    mejor_vehiculo = v

        if mejor_ruta:
            rutas_totales.append({
                "vehiculo": mejor_vehiculo,
                "ruta": mejor_ruta,
                "coste": mejor_costo,
                "distancia": calcular_distancia(mejor_ruta),
                "carga": calcular_carga(mejor_ruta)
            })
            coste_total += mejor_costo

            # Eliminar clientes atendidos de la lista de pendientes
            for cliente in mejor_ruta:
                if cliente in clientes_pendientes:
                    clientes_pendientes.remove(cliente)
        else:
            break

    return rutas_totales, coste_total

# Función para recalcular rutas
def recalcular_rutas(rutas_totales):
    for ruta in rutas_totales:
        mejor_vehiculo = ruta["vehiculo"]
        mejor_costo = ruta["coste"]

        for v in vehiculos:
            if v == ruta["vehiculo"]:
                continue

            distancia = calcular_distancia(ruta["ruta"])
            carga = calcular_carga(ruta["ruta"])
            if distancia <= autonomia[v] and carga <= capacidad_vehiculo[v]:
                nuevo_costo = distancia * coste_km[v]
                if nuevo_costo < mejor_costo:
                    mejor_vehiculo = v
                    mejor_costo = nuevo_costo

        ruta["vehiculo"] = mejor_vehiculo
        ruta["coste"] = mejor_costo
        ruta["distancia"] = calcular_distancia(ruta["ruta"])  # Actualizar distancia
        ruta["carga"] = calcular_carga(ruta["ruta"])  # Actualizar carga


def hill_climbing():
    rutas_totales, coste_total = distribuir_rutas_cooperativa()
    rutas_finales = []
    for i,k in enumerate(rutas_totales):
        k['vehicle'] = k.pop('vehiculo')
        k['clientes'] = k.pop('ruta')
        k['peso_total'] = k.pop('carga')
        k['distancia_total'] = k.pop('distancia')
        k['costo_total'] = k.pop('coste')
        rutas_finales.append([i,k])
    
    return rutas_finales
