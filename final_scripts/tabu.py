import pandas as pd
import numpy as np
import random


# Función encargada de calcular el coste total de una ruta
def calculate_route_distance(route, distance_matrix, cost_per_unit):
    distance = 0
    for i in range(len(route) - 1):
        dist = distance_matrix[route[i]][route[i + 1]]
        if dist == 0:
            return float('inf')
        distance += dist * cost_per_unit
    return distance

# Función encargada de verificar si una ruta es válida
def is_valid_route(route, demandas, capacity):
    total_demand = sum(demandas[cliente] for cliente in route)
    return total_demand <= capacity

# Función encargada de generar rutas iniciales válidas
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

# Función encargada de calcular la distancia total de un conjunto de rutas
def calculate_total_distance(routes, distance_matrix, costes):
    total_distance = 0
    for route, cost in zip(routes, costes):
        total_distance += calculate_route_distance(route, distance_matrix, cost)
    return total_distance

# Función encargada de generar vecinos
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

# Función encargada de ejecutar el algoritmo de Tabú Search
def tabu_search_multiple_tsp(distance_matrix, initial_routes, max_iterations, tabu_size, almacen, costes, demandas, capacidades, max_no_improve=20):
    current_routes = initial_routes
    best_routes = current_routes
    best_distance = calculate_total_distance(current_routes, distance_matrix, costes)
    tabu_list = []
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

        print(f"Generación {iteration}: Mejor distancia encontrada: {best_distance}")
        # Verificar criterio de parada adicional
        if no_improve_counter >= max_no_improve:
            #   print(f"Parada anticipada: {no_improve_counter} iteraciones sin mejora.")
            break

    return best_routes, best_distance

# Función encargada de generar el resumen de las rutas
def generate_route_summary(routes, clients_names, distance_matrix, costes, num_vehicles):
    summary = []

    for i, route in enumerate(routes):
        clientes = [clients_names[client] for client in route]
        distancia_total = sum(distance_matrix[route[j]][route[j+1]] for j in range(len(route) - 1))
        costo_total = distancia_total * costes[i % num_vehicles]
        vehicle = (i % num_vehicles) + 1
        route_info = {
            "clientes": clientes,
            "distancia_total": round(distancia_total, 2),
            "costo_total": round(costo_total, 2),
            "vehicle": vehicle
        }

        summary.append([i, route_info])

    return summary

# Función principal de Tabú Search
def tabu_search():

    df_location = pd.read_excel('df_location.xlsx')
    df_distance = pd.read_excel('df_distance_km.xlsx')
    df_vehicle = pd.read_excel('df_vehicle.xlsx')
    df_orders = pd.read_csv('df_order.csv')

    clients_names = df_location['cliente'].to_list()
    clients_coords = df_location[['Latitud','Longitud']].to_numpy()

    clients = {name: coord for name, coord in zip(clients_names, clients_coords)}

    distances_matrix = df_distance.to_numpy()

    almacen = len(clients_names) - 1
    num_vehicle = 5
    costes = df_vehicle['costo_km'].to_list()
    capacidades = df_vehicle['capacidad_kg'].to_list()
    demandas_dict = dict(zip(df_orders["cliente"], df_orders["order_demand"]))
    demandas = [demandas_dict.get(client, 0) for client in clients_names]

    initial_routes = generate_valid_initial_routes(distances_matrix, num_vehicle, almacen, demandas, capacidades)

    # Parámetros iniciales
    max_iterations = 1000
    tabu_size = 10  # Tamaño de la lista Tabú
    max_no_improve = 200  # Número máximo de iteraciones sin mejora

    # Ejecutar Tabu Search
    mejor_solucion, costo_mejor_solucion = tabu_search_multiple_tsp(
        distances_matrix, initial_routes, max_iterations, tabu_size, almacen, costes, demandas, capacidades, max_no_improve=max_no_improve
    )

    # Generar la salida estructurada
    resumen_rutas = generate_route_summary(mejor_solucion, clients_names, distances_matrix, costes, num_vehicle)

    modelo_tabu = {
        "rutas": resumen_rutas,
        "costo_total": round(costo_mejor_solucion, 2)
    }

    return modelo_tabu


