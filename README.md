# README: Optimización de Rutas y Predicción de Pedidos de Alimentos Perecederos

## Índice
1. [Descripción del Proyecto](#descripción-del-proyecto)
2. [Funcionalidades Principales](#funcionalidades-principales)
3. [Tecnologías Utilizadas](#tecnologías-utilizadas)
4. [Instalación](#instalación)
5. [Estructura del Proyecto](#estructura-del-proyecto)
6. [Uso del Sistema](#uso-del-sistema)
7. [Datos y Modelos](#datos-y-modelos)
8. [Contribuciones](#contribuciones)
9. [Licencia](#licencia)
10. [Contacto](#contacto)

---

## Descripción del Proyecto

Este proyecto tiene como objetivo mejorar la eficiencia en la distribución y gestión de alimentos perecederos mediante dos componentes clave:
- **Optimización de Rutas**: Diseñar rutas óptimas para minimizar costos logísticos y garantizar la frescura de los productos.
- **Predicción de Pedidos**: Utilizar modelos de machine learning para predecir demandas futuras y ajustar inventarios de manera precisa.

El sistema está desarrollado con una arquitectura moderna que incluye una base de datos MySQL, una API RESTful construida con Django y Django REST Framework, y una interfaz de usuario interactiva desarrollada en React.js.

---

## Funcionalidades Principales

- **Optimización de Rutas**:
  - Algoritmos avanzados para calcular las rutas más eficientes considerando factores como distancia, tiempo de entrega y condiciones climáticas.
  - Integración con APIs de mapas (Google Maps, OpenStreetMap, etc.).

- **Predicción de Pedidos**:
  - Modelos de regresión y series temporales para estimar la demanda futura basada en datos históricos.
  - Incorporación de variables externas (feriados, promociones, tendencias estacionales).

- **Visualización de Datos**:
  - Dashboards interactivos desarrollados en React.js para analizar resultados de optimización y predicciones.
  - Gráficos y mapas dinámicos para facilitar la interpretación.

- **Gestión de Inventarios**:
  - Herramientas para ajustar niveles de inventario según las predicciones generadas.

---

## Tecnologías Utilizadas

- **Backend**:
  - **Framework**: Django + Django REST Framework
  - **Base de Datos**: MySQL
  - **Lenguaje**: Python

- **Frontend**:
  - **Framework**: React.js
  - **Herramientas de Visualización**: Chart.js, Openlayers (para mapas)

- **Modelos de Machine Learning**:
  - TensorFlow, Scikit-learn, Pandas, NumPy

- **APIs Externas**:
  - Google Maps API (para optimización de rutas).
  - Weather API (para condiciones climáticas).

- **Despliegue**:
  - Docker (para contenerización).
  - Nginx (servidor web para el frontend).

---

## Instalación

### Backend (Django + Django REST Framework)

1. **Clonar el Repositorio**:

   ```bash
    git clone https://github.com/kikemocha/Distribution_of_perishable_goods.git
    cd backend
    ```

2. **Crear y Activar el Entorno Virtual:**

     ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```  

3. **Instalar dependecias:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configurar Base de Datos MySQL:**

    - Asegúrate de tener MySQL instalado y configurado.
    - Actualiza las credenciales de la base de datos en `settings.py`.

5. **Aplicar Migraciones:**
    ```bash
    python manage.py migrate
    ```

6. **Iniciar el Servidor de Desarrollo:**
    ```bash
    python manage.py runserver
    ```

### Frontend (React.js)

1. **Navegar al Directorio del Frontend:**

   ```bash
    cd frontend
    ```
    
2. **Instalar Dependencias:**

     ```bash
    npm install
    ```  

3. **Iniciar el Servidor de Desarrollo:**
    ```bash
    npm start
    ```

---

## Estructura del Proyecto

```bash
    /backend_proyect_1
    │
    ├── cart
    │   ├── __pycache__
    │   ├── migrations
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── tests.py
    │   └── views.py
    │
    ├── orders
    │   ├── __pycache__
    │   ├── migrations
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── serializers.py
    │   ├── tests.py
    │   └── views.py
    │
    ├── products
    │   ├── __pycache__
    │   ├── migrations
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── insert_data.py
    │   ├── models.py
    │   ├── serializers.py
    │   ├── tests.py
    │   └── views.py
    │
    ├── vehicles
    │   ├── __pycache__
    │   ├── migrations
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── serializers.py
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    │
    ├── manage.py
    │── settings.py    
    │
    ├── /datasets
    │    ├── df_distance_km.xlsx
    │    ├── df_distance_min.xlsx
    │    ├── df_historic_order_demand.xlsx
    │    ├── df_location.xlsx
    │    ├── df_orders.xlsx
    │    └── df_vehicle.xlsx
    │
    final_scripts/
    │   ├──caso2.txt
    │   ├──df_distance_km.xlsx
    │   ├──df_location.xlsx
    │   ├──df_order.csv
    │   ├──df_vehicle.xlsx
    │   ├──genetico.py
    │   ├──hill_climbing.py
    │   ├──main.py
    │   ├──tabu.py
    │
    │───__pycache__/
    │
    frontend_proyect_1/
    │   .gitignore
    │   package-lock.json
    │   package.json
    │   README.md
    │   tailwind.config.js
    │
    ├───public/
    │
    ├───src/
    │   ├──App.css
    │   ├──App.js
    │   ├──App.test.js
    │   ├──index.css
    │   ├──index.js
    │   ├──reportWebVitals.js
    │   ├──setupTests.js
    │   ├──types.ts
    │   │
    │   ├───Components/
    │   │   ├──cartProducts.tsx
    │   │   ├──ProductPopUp.tsx
    │   │   ├──Products.jsx
    │   │   ├──regions.js
    │   │
    │   ├───Context/
    │   │   ├──CartContext.tsx
    │   │
    │   ├───Pages/
    │   │   ├──AdminPage.jsx
    │   │   ├──HomePage.jsx
    │   │   ├──VehiclesForm.jsx

```

---

## Uso del sistema

### Optimización de Rutas

1. Ingresa los puntos de origen y destino en la interfaz de React.
2. Configura restricciones adicionales (horarios, capacidades de vehículos).
3. Genera y visualiza la ruta recomendada en el mapa interactivo.

### Predicción de Pedidos

1. Sube o carga datos históricos de ventas desde la interfaz.
2. Selecciona el período futuro a predecir.
3. Ver los resultados en formato tabular y gráfico.