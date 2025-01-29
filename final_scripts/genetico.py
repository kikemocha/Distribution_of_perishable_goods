import numpy as np
import pandas as pd
import random
import copy

matrix_km = pd.read_excel('df_distance_km.xlsx')
matrix_km.index = matrix_km.columns

class Vehicle():
    def __init__(self, id, capacidad_kg, costo_km, autonomia_km):
        self.id = id
        self.capacidad_kg = capacidad_kg
        self.costo_km = costo_km
        self.autonomia_km = autonomia_km
    def get_price(self, distance):
        return round(self.costo_km * distance, 2)

class Client():
    def __init__(self, cliente, order_kg):
        self.cliente = cliente
        self.order_kg = order_kg

class Order():
    def __init__(self, clients, vehicle, route):
        self.clients = clients
        self.vehicle = vehicle
        self.route = route

    def get_clients(self):
        return self.clients
    
    def get_kg(self):
        return [i.order_kg for i in self.clients]
    
    def get_route(self):
        final_route = []
        for i in self.route:
            if i == 'Almacén':
                final_route.append([i, 0])
            for client in self.clients:
                if client.cliente == i:
                    final_route.append([i, client.order_kg])
        return final_route

def check_viability(ruta):
    for i in range(0,len(ruta)-1,1):
        try:
            if matrix_km[ruta[i].client][ruta[i+1].cliente] == 0:
                return False
        except:
            pass
    return True

def check_viability_client(ruta):
    for i in range(0,len(ruta)-1,1):
        try:
            if (matrix_km[ruta[i]][ruta[i+1]] != 0) == False:
                return False
        except:
            pass
    return True


def create_route(clients):
    random.shuffle(clients)
    route = clients
    while check_viability(route) == False:
        random.shuffle(clients)
        ['Almacén'] + clients + ['Almacén']
    return route





def generate_initial_solution(vehicles, route, clientes):
    solucion = {}
    clients = [i.cliente for i in route]
    random.shuffle(clients)

    vh_copy = vehicles.copy()
    random.shuffle(vh_copy)

    route_vehicles = vh_copy

    ruta = ['Almacén'] + [i.cliente for i in route] + ['Almacén']
    counter = 0
    while clients:
        bucle = True
        vehiculo = random.choice(route_vehicles)

        solucion[vehiculo.id] = {
            'clientes' : [],
            'distancia_total' : 0,
            'peso_total' : 0,
            'costo_total' : 0
        }

        carga_actual = 0
        distancia_actual = 0
        while clients and bucle:
            temp_route = ruta[counter:counter+2]
            distance = matrix_km[temp_route[0]][temp_route[1]]
            distance_to_warehouse = matrix_km[temp_route[0]]['Almacén']
            load = [i.order_kg for i in clientes if i.cliente == temp_route[1]][0]

            if (carga_actual+load)<=vehiculo.capacidad_kg and (distancia_actual+distance+distance_to_warehouse)<=vehiculo.autonomia_km:
                if distancia_actual == 0:
                    distancia_actual += (distance +distance_to_warehouse)
                else:
                    distancia_actual += distance
                carga_actual += load
                del clients[0]
                solucion[vehiculo.id]['clientes'].append(temp_route[1])
                counter += 1
            else:
                solucion[vehiculo.id]['distancia_total'] += round((distancia_actual+distance_to_warehouse),2)
                solucion[vehiculo.id]['peso_total'] += carga_actual
                solucion[vehiculo.id]['costo_total'] += round(vehiculo.costo_km * (distancia_actual+distance_to_warehouse),2)
                route_vehicles.remove(vehiculo)
                bucle = False
            
        if len(clients) < 1:
            ultima_parada = ruta[-2]
            distancia_regreso = matrix_km[ultima_parada]['Almacén']
            solucion[vehiculo.id]['distancia_total'] += round(distancia_actual,2)
            solucion[vehiculo.id]['peso_total'] += carga_actual
            solucion[vehiculo.id]['costo_total'] += round(vehiculo.costo_km * distancia_actual,2)
            if distancia_regreso<=vehiculo.autonomia_km:
                distancia_actual += distancia_regreso
            #else:
            #    route_vehicles.remove(vehiculo)
    if check_viability_client([cliente for sublista in [k['clientes'] for i,k in solucion.items()] for cliente in sublista]) : 
        return(solucion)
    else:
        return 9999




def fitness(solution):
    if solution == 9999:
        return -9999
    else:
        total_cost = 0
        for vehicle_id, details in solution.items():
            total_cost += details['costo_total']
        return -total_cost

def create_population(clients, size):
    population = []
    for _ in range(size):
        route = create_route(clients)
        population.append(route)
    return population


def selection(population, results, tournament_size=5):
    tournament = random.sample(list(zip(population, results)), tournament_size)
    tournament.sort(key=lambda x: x[1], reverse=True)
    return [i[0] for i in tournament[0:2]]

def crossover(parents):
    parent1, parent2 = parents
    midpoint = len(parent1) // 2
    child = parent1[:midpoint] + [client for client in parent2 if client not in parent1[:midpoint]]
    
    if check_viability(child):
        return child
    else:
        return parent1


def mutate(route, mutation_rate=0.1):
    route_inicial = route.copy()
    if  random.random() < mutation_rate:
        i, j = random.sample(range(0,len(route)), 2)
        route[i], route[j] = route[j], route[i]
    if check_viability(route):
        return route
    else:
        return route_inicial


def genetic_algorithm(clients, vehicles, population_size=100, generations=200, mutation_rate=0.2):
    population = create_population(clients, population_size)
    results = [fitness(generate_initial_solution(vehicles=vehicles, route=i, clientes=clients)) for i in population ]
    routes = []

    for generation in range(generations):
        new_population = []
        new_results = []
        new_routes = []
        
        for _ in range(population_size):
            parents = selection(population, results)
            child = crossover(parents)
            child = mutate(child, mutation_rate)
            new_population.append(child)
        
        for j in new_population:
            route = generate_initial_solution(vehicles, j, clients)
            route_value = fitness(route)

            new_results.append(route_value)
            new_routes.append(route)
        
        population = new_population
        results = new_results
        routes = new_routes

        # Mejor solución en la generación actual
        best_cost = min([i for i in results if i != -9999])
        #print(f"Generación {generation}: Mejor costo: {-best_cost}")  # Invertir para mostrar el costo original
    
    # Mejor solución final
    best_index = results.index(max(results))  # Seleccionar el mejor fitness
    
    return population[best_index], -results[best_index], routes[best_index]  # Retornar ruta y costo


def algoritmo_genetico():
    clientes = []
    vehicles = []

    for _, row in pd.read_excel('df_vehicle.xlsx').iterrows():
        vehicles.append(Vehicle(
            id = int(row['vehiculo_id']), 
            capacidad_kg= float(row['capacidad_kg']),
            costo_km= float(row['costo_km']), 
            autonomia_km= int(row['autonomia_km'])
            ))
    
    for _, row in pd.read_csv('df_order.csv').iterrows():
        cliente = row['cliente']
        order_demand = row['order_demand']
        clientes.append(Client(cliente, order_demand))
    
    best_population, best_cost, route = genetic_algorithm(clientes, vehicles, population_size=100, generations=1000, mutation_rate=0.2)
    final_routes = []
    for i, k in enumerate(route):
        route[k]['vehicle'] = k
        final_routes.append([i,route[k]])
    return(final_routes)
