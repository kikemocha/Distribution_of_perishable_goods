from genetico import algoritmo_genetico
from hill_climbing import hill_climbing
from tabu import tabu_function

result1 = algoritmo_genetico()
result2 = hill_climbing()
result3 = tabu_function()

print('Hill Climbing:', result2)
print()
print('Tabú: ', result3)
print()
print('Genético: ',result1)
print()
