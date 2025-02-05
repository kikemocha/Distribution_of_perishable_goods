from genetico import algoritmo_genetico
from hill_climbing import hill_climbing
from tabu import tabu_search
import pandas as pd

def formatear_texto(texto):
    print(f'Nº RUTA: {texto[0]}')
    print(f"Vehículo: {texto[1]['vehicle']}")
    print(f"Ruta: {texto[1]['clientes']}")
    print(f"Peso Total: {texto[1]['peso_total']}")
    print(f"Distancia Total: {texto[1]['distancia_total']}")
    print(f"Costo Total: {texto[1]['costo_total']} €")
    print()

def formatear_texto_tabu(texto):
    print(f'Nº RUTA: {texto[0]}')
    print(f"Vehículo: {texto[1]['vehicle']}")
    print(f"Ruta: {texto[1]['clientes']}")
    print(f"Distancia Total: {texto[1]['distancia_total']} km")
    print(f"Costo Total: {texto[1]['costo_total']} €")
    print()
    
df_vechicle = pd.read_excel('df_vehicle.xlsx')
print(df_vechicle)
print()

try:
    result1 = algoritmo_genetico()
    print('Algorítmo Genético:')
    print(result1)
    for ruta in result1:   
        formatear_texto(ruta)
    print()
except:
    print('Genético no se pudo')
try:
    result2 = hill_climbing()
    print('Hill Climbing:')
    for ruta in result2:
        formatear_texto(ruta)
    print()
except:
    print('Hill Climbing no se pudo')
try:
    result3 = tabu_search()
    print('Tabú Search:')
    for ruta in result3['rutas']:
        formatear_texto_tabu(ruta)
    print()
    print('Costo Total Tabu Search:', result3['costo_total'])
except Exception as e:   
    print('Tabú Search no se pudo', e)


