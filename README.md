# TSLib Shiny App

Una aplicación web profesional para análisis de series temporales usando TSLib como backend.

## Características

- 🎯 **Interfaz intuitiva** para usuarios no técnicos
- 📊 **Visualizaciones interactivas** con Plotly
- 🔧 **Configuración flexible** de modelos ARIMA
- 📈 **Análisis completo** con diagnósticos y predicciones
- 🎨 **Diseño profesional** y minimalista

## Instalación

1. **Clonar el repositorio:**
```bash
git clone <repository-url>
cd tslib-shiny-app
```

2. **Crear entorno virtual:**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación:**
```bash
python app.py
```

5. **Abrir en el navegador:**
La aplicación estará disponible en `http://localhost:8000`

## Uso

### Flujo de Trabajo

1. **Cargar Datos**: Sube un archivo CSV/Excel o usa datos de ejemplo
2. **Explorar**: Visualiza la serie temporal y estadísticas básicas
3. **Configurar**: Ajusta parámetros del modelo ARIMA (p, d, q)
4. **Ajustar**: Entrena el modelo con tus datos
5. **Diagnosticar**: Revisa gráficos de residuos y métricas
6. **Predecir**: Genera predicciones futuras con intervalos de confianza

### Datos de Ejemplo

La aplicación incluye tres datasets de ejemplo:
- **airline_passengers.csv**: Serie clásica con tendencia y estacionalidad
- **temperature.csv**: Temperatura diaria con variaciones suaves
- **sales.csv**: Ventas mensuales con tendencia y ruido

## Estructura del Proyecto

```
tslib-shiny-app/
├── app.py                    # Aplicación principal
├── ui/                       # Componentes de interfaz
│   ├── components.py        # Componentes reutilizables
│   └── layouts.py           # Layouts y estructura
├── server/                   # Lógica del servidor
│   ├── data_handler.py      # Procesamiento de datos
│   ├── model_handler.py     # Ajuste de modelos
│   └── visualization.py     # Generación de gráficos
├── utils/                    # Utilidades
│   └── tslib_interface.py   # Interface con TSLib
├── data/examples/           # Datos de ejemplo
├── static/                  # Assets estáticos (CSS)
└── requirements.txt         # Dependencias
```

## Tecnologías

- **Shiny for Python**: Framework web reactivo
- **TSLib**: Librería de análisis de series temporales
- **Plotly**: Visualizaciones interactivas
- **Pandas**: Manipulación de datos
- **NumPy**: Operaciones numéricas

## Desarrollo

### Arquitectura Event-Driven

La aplicación sigue un paradigma orientado a eventos:
- **UI Components**: Elementos de interfaz con IDs únicos
- **Event Handlers**: Funciones que responden a interacciones del usuario
- **Estado Reactivo**: Variables que almacenan el estado actual

### Agregar Nuevos Componentes

1. Crear función en `ui/components.py`
2. Agregar event handler en `app.py`
3. Actualizar layout en `ui/layouts.py`

## Contribuir

1. Fork el proyecto
2. Crear rama para feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## Licencia

MIT License - Ver [LICENSE](LICENSE) para más detalles.

## Autores

- **Genaro Melgar** - ESCOM, Instituto Politécnico Nacional
