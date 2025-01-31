import pandas as pd
import numpy as np
import random

df_location = pd.read_excel('df_location.xlsx')
df_distance = pd.read_excel('df_distance_km.xlsx')
df_vehicle = pd.read_excel('df_vehicle.xlsx')
df_orders = pd.read_csv('df_order.csv')

clients_names = df_location['Cliente'].to_list()
clients_coords = df_location[['Latitud','Longitud']].to_numpy()

clients = {name: coord for name, coord in zip(clients_names, clients_coords)}

distances_matrix = df_distance.to_numpy()

def calculate_route_distance(route, distance_matrix, cost_per_unit):
    distance = 0
    for i in range(len(route) - 1):
        dist = distance_matrix[route[i]][route[i + 1]]
        if dist == 0:
            return float('inf')
        distance += dist * cost_per_unit
    return distance

def is_valid_route(route, demandas, capacity):
    total_demand = sum(demandas[cliente] for cliente in route)
    return total_demand <= capacity

def generate_valid_initial_routes(distance_matrix, num_vehiculos, almacen, demandas, capacidades):
    clientes = [cliente for cliente in range(len(distance_matrix)) if cliente != almacen]
    valid_routes_found = False
    while not valid_routes_found:
        random.shuffle(clientes)
        routes = [[almacen] for _ in range(num_vehiculos)]
        for cliente in clientes:
            for route in routes:
                if sum(demandas[r] for r in route) + demandas[cliente] <= capacidades[routes.index(route)]:
                    route.append(cliente)
                    break
        for route in routes:
            route.append(almacen)
        if all(calculate_route_distance(route, distance_matrix, 1) != float('inf') for route in routes):
            valid_routes_found = True
    return routes

def calculate_total_distance(routes, distance_matrix, costes):
    total_distance = 0
    for route, cost in zip(routes, costes):
        total_distance += calculate_route_distance(route, distance_matrix, cost)
    return total_distance

def generate_vecinos_multiple(routes, almacen, demandas, capacidades):
    neighbors = []
    for i in range(len(routes)):
        for j in range(len(routes)):
            if i != j:
                for k in range(1, len(routes[i]) - 1):
                    for l in range(1, len(routes[j]) - 1):
                        neighbor = [route[:] for route in routes]
                        neighbor[i][k], neighbor[j][l] = neighbor[j][l], neighbor[i][k]
                        if is_valid_route(neighbor[i], demandas, capacidades[i]) and is_valid_route(neighbor[j], demandas, capacidades[j]):
                            neighbors.append(neighbor)
    return neighbors

def tabu_search_multiple_tsp(distance_matrix, initial_routes, max_iterations, tabu_size, almacen, costes, demandas, capacidades, max_no_improve=20):
    current_routes = initial_routes
    best_routes = current_routes
    best_distance = calculate_total_distance(current_routes, distance_matrix, costes)
    tabu_list = []
    historial = []
    no_improve_counter = 0

    for iteration in range(max_iterations):
        neighbors = generate_vecinos_multiple(current_routes, almacen, demandas, capacidades)
        evaluated_neighbors = [(neighbor, calculate_total_distance(neighbor, distance_matrix, costes)) 
                               for neighbor in neighbors if neighbor not in tabu_list]

        if not evaluated_neighbors:
            break  # Si no hay vecinos válidos, detener el algoritmo

        best_neighbor, best_neighbor_distance = min(evaluated_neighbors, key=lambda x: x[1])
        
        current_routes = best_neighbor
        if best_neighbor_distance < best_distance:
            best_routes = best_neighbor
            best_distance = best_neighbor_distance
            no_improve_counter = 0
        else:
            no_improve_counter += 1 

        # Actualizar lista Tabú
        tabu_list.append(best_neighbor)
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

        # Guardar historial
        historial.append((best_neighbor, best_neighbor_distance))

        # Verificar criterio de parada adicional
        if no_improve_counter >= max_no_improve:
            #   print(f"Parada anticipada: {no_improve_counter} iteraciones sin mejora.")
            break

    return best_routes, best_distance, historial

almacen = len(clients_names) - 1
num_vehicle = 5
costes = df_vehicle['costo_km'].to_list()
capacidades = df_vehicle['capacidad_kg'].to_list()
demandas_dict = dict(zip(df_orders["cliente"], df_orders["order_demand"]))
demandas = [demandas_dict.get(client, 0) for client in clients_names]

initial_routes = generate_valid_initial_routes(distances_matrix, num_vehicle, almacen, demandas, capacidades)

# Parámetros iniciales
max_iterations = 100
tabu_size = 10
max_no_improve = 20  # Número máximo de iteraciones sin mejora

# Ejecutar Tabu Search
mejor_solucion, costo_mejor_solucion, historial = tabu_search_multiple_tsp(
    distances_matrix, initial_routes, max_iterations, tabu_size, almacen, costes, demandas, capacidades, max_no_improve=max_no_improve
)

def convert_routes_to_coordinates(routes, clients):
    routes_with_coordinates = []
    for route in routes:
        route_coords = [tuple(clients[clients_names[client]]) for client in route]
        routes_with_coordinates.append(route_coords)
    return routes_with_coordinates

mejor_solucion_coords = convert_routes_to_coordinates(mejor_solucion, clients)

# Guardar el modelo
modelo_tabu = {
    "mejor_solucion": mejor_solucion_coords,
    "costo_mejor_solucion": costo_mejor_solucion,
    "parametros": {
        "tamano_tabu": tabu_size,
        "max_iteraciones": max_iterations,
        "criterio_parada": f"Sin mejora en {max_no_improve} iteraciones"
    },
    "historial": historial
}

def calc_cost_km(vehicle, route):
    clients = [i for i in route if i != 'Almacén']
    peso_total = sum([df_orders[df_orders['cliente'] == cliente]['order_demand'].iloc[0] for cliente in clients])
    total_km = 0
    df_distance_aux = df_distance.copy()
    df_distance_aux.index = df_distance_aux.columns
    for i in range(len(route)-1):
        client_1 = route[i]
        client_2 = route[i+1]
        total_km += df_distance_aux[client_1][client_2]
    cost_vehicle = df_vehicle[df_vehicle['vehiculo_id'] == vehicle]['costo_km'].iloc[0]
    precio_cost = round(total_km * cost_vehicle,2)
    return precio_cost, round(total_km,2), peso_total


def tabu_function():
    try:
        rutas_finales = []
        for i, ruta in enumerate(modelo_tabu['mejor_solucion']):
            ruta = [df_location[(df_location['Latitud'] == cliente[0]) & (df_location['Longitud'] == cliente[1])]['Cliente'].iloc[0] for cliente in ruta]
            cost, km, peso_total = calc_cost_km(i+1, ruta)
            rutas_finales.append([i, {'vehicle': i+1,'clientes': ruta, 'distancia_total': km, 'peso_total': peso_total, 'costo_total': cost}])
        return rutas_finales
    except Exception as e:
        return e

