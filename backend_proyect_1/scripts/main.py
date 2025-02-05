import pandas as pd
import os
import json
import asyncio
import subprocess
from hill_climbing import hill_climbing
from genetico import algoritmo_genetico

async def run_distance_script():
    script_path = os.path.join(os.path.dirname(__file__), "generate_distance_km.py")
    process = await asyncio.create_subprocess_exec(
        "python3", script_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    if process.returncode == 0:
        print("✅ Script de distancia ejecutado correctamente.")
        return True
    else:
        print(f"❌ Error en el script:\n{stderr.decode()}")
        return False

async def process_orders():
    try:

        print("⏳ Calculando la matriz de distancias...")
        success = await run_distance_script()
        if not success:
            return json.dumps({"status": "error", "message": "Error al calcular matriz de distancias."})

        # Ejecutar los algoritmos (de forma sincrónica)
        genetico_result = algoritmo_genetico()
        hill_climbing_result = hill_climbing()

        result_dict = {
            "status": "success",
            "algorithms": {
                "genetico": genetico_result,
                "hill_climbing": hill_climbing_result
            }
        }
        return json.dumps(result_dict, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

if __name__ == "__main__":
    result = asyncio.run(process_orders())
    print(result)
