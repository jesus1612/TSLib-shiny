# TSLib Shiny App - Análisis de Series de Tiempo

Una aplicación web interactiva desarrollada con **Shiny for Python** para análisis avanzado de series de tiempo usando la librería TSLib.

## 🚀 Características

- **Pipeline completo** de análisis de series de tiempo
- **Interfaz wizard/stepper** intuitiva
- **Tema oscuro profesional** 
- **Arquitectura basada en eventos** reactivos
- **Organización modular** por features
- **Procesamiento distribuido** (preparado para PySpark)

## 📋 Pipeline de Análisis

1. **📁 Upload** - Carga de datasets locales
2. **📊 Visualization** - Visualización y estadísticas iniciales  
3. **⚙️ Model Selection** - Selección de modelos ARIMA
4. **🔄 Execution** - Ejecución de algoritmos en servidor
5. **📈 Results** - Visualización de resultados y métricas
6. **📄 Reports** - Generación de reportes descargables

## 🛠️ Instalación

### Prerrequisitos
- Python 3.8+
- pip

### Pasos de instalación

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd tslib-shiny-app
```

2. **Instalar dependencias (crea entorno virtual automáticamente)**
```bash
make install
```

El Makefile detectará automáticamente si necesitas un entorno virtual y lo creará por ti.

3. **Ejecutar la aplicación**
```bash
make run
# o manualmente:
python app.py
```

4. **Abrir en el navegador**
La aplicación estará disponible en: `http://localhost:8000`

## 📁 Estructura del Proyecto

```
tslib-shiny-app/
├── app.py                    # Entry point
├── features/                 # Módulos por feature
│   ├── upload/              # Carga de datos
│   ├── visualization/       # Visualización
│   ├── model_selection/     # Selección de modelos
│   ├── execution/           # Ejecución
│   ├── results/             # Resultados
│   └── reports/             # Reportes
├── components/              # Componentes reutilizables
├── static/                  # CSS y assets
├── data/examples/           # Datasets de ejemplo
├── requirements.txt         # Dependencias
├── Makefile                # Comandos de desarrollo
└── README.md               # Este archivo
```

## 🎯 Uso

1. **Cargar datos**: Sube un archivo CSV/Excel con tu serie temporal
2. **Explorar**: Visualiza la serie y analiza estadísticas básicas
3. **Configurar**: Selecciona parámetros del modelo ARIMA
4. **Ejecutar**: Inicia el análisis en el servidor
5. **Evaluar**: Revisa resultados y métricas de rendimiento
6. **Exportar**: Descarga reportes y datos procesados

## 📊 Datasets de Ejemplo

El proyecto incluye datasets de ejemplo en `data/examples/`:
- `sales.csv` - Serie temporal de ventas
- `temperature.csv` - Serie de temperaturas

## 🛠️ Comandos de Desarrollo

```bash
make install    # Instalar dependencias (crea venv automáticamente)
make run        # Ejecutar aplicación (requiere venv)
make clean      # Limpiar archivos temporales
make clean-all  # Limpiar todo incluyendo entorno virtual
make format     # Formatear código
make help       # Ver ayuda
```

### ⚠️ Notas Importantes:
- **`make run` requiere entorno virtual**: Si no existe, te pedirá ejecutar `make install` primero
- **`make install` es inteligente**: Crea el entorno virtual automáticamente si no existe
- **`make clean-all`**: Elimina completamente el entorno virtual si necesitas empezar de cero

## 🏗️ Arquitectura

- **Frontend**: Shiny UI con componentes reactivos
- **Backend**: Lógica de procesamiento con TSLib
- **Paradigma**: Event-driven programming
- **Estado**: Reactive values y session state
- **Estilos**: CSS custom con tema oscuro

## 🔧 Tecnologías

- **Shiny for Python** - Framework web reactivo
- **TSLib** - Librería de análisis de series de tiempo
- **Pandas/NumPy** - Manipulación de datos
- **Matplotlib/Plotly** - Visualizaciones
- **PySpark** - Procesamiento distribuido (opcional)

## 📝 Notas de Desarrollo

- **UI en español**, comentarios en inglés
- **Placeholders** para funcionalidad backend
- **Tema oscuro** profesional
- **Responsive design** básico
- **Arquitectura escalable** para futuras funcionalidades

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🆘 Soporte

Si tienes problemas o preguntas:
- Abre un issue en GitHub
- Revisa la documentación de [Shiny for Python](https://shiny.posit.co/py/)
- Consulta la documentación de TSLib

---

**Desarrollado con ❤️ para análisis avanzado de series de tiempo**
