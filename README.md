# TSLib Shiny App – Análisis de Series de Tiempo

Aplicación web interactiva (Shiny for Python) para análisis de series de tiempo usando la librería **TSLib**. Parte del proyecto de titulación sobre paralelización de procesos en series de tiempo; este repo es la interfaz; el núcleo algorítmico está en el repositorio **time-series-library**.

## Características

- Pipeline guiado (wizard/stepper): carga → visualización → selección de modelo → ejecución → resultados → reportes.
- Modelos AR, MA, ARMA y ARIMA con auto-selección de orden vía TSLib.
- Validación de datos (TSLib `DataValidator`), ACF/PACF, pronósticos e intervalos de confianza.
- Tema oscuro, UI en español, arquitectura por features.

## Requisitos

- Python 3.8+
- **TSLib** instalado en el mismo entorno (repositorio `time-series-library`). Ver [Integración con TSLib](#integración-con-tslib).

## Instalación

```bash
git clone <url-repo-tslib-shiny-app>
cd tslib-shiny-app
make install   # crea venv si no existe e instala dependencias
```

Instalar TSLib (desde la ruta donde clonaste **time-series-library**):

```bash
pip install -e /ruta/absoluta/time-series-library
```

En `requirements.txt` hay una nota con la ruta; ajústala a tu máquina.

## Ejecución

```bash
make run
# o: source venv/bin/activate && python app.py
```

Abrir en el navegador: `http://localhost:8000`.

## Estructura del Proyecto y Archivos

```
tslib-shiny-app/
├── app.py                      # Entry point Shiny; orquestación de pasos y estado
├── components/
│   ├── __init__.py
│   ├── layout.py               # Layout principal (sidebar, stepper, contenedores)
│   └── stepper.py              # Componente de pasos del wizard
├── features/                   # Módulos por paso del pipeline
│   ├── upload/
│   │   └── ui.py               # Carga CSV/Excel, selección de columnas, validación
│   ├── visualization/
│   │   └── ui.py               # Gráfico de serie, estadísticas, ACF/PACF
│   ├── model_selection/
│   │   └── ui.py               # Selector de modelo (AR/MA/ARMA/ARIMA) y parámetros
│   ├── execution/
│   │   └── ui.py               # Botón ejecutar, log de progreso
│   ├── results/
│   │   └── ui.py               # Métricas, pronóstico, diagnósticos, exportar
│   └── reports/
│       └── ui.py               # Generación de reportes (en desarrollo)
├── services/
│   ├── __init__.py
│   └── tslib_service.py        # Capa de integración con TSLib (validación, fit, pronóstico, etc.)
├── static/
│   └── styles.css              # Estilos y tema oscuro
├── data/
│   └── examples/
│       ├── generate_dummy_data.py   # Genera CSV de ejemplo con faltantes opcionales
│       └── dummy_with_missing.csv   # Datos de ejemplo
├── requirements.txt
├── Makefile                    # install, run, clean, format
├── README.md                   # Este archivo
├── INTEGRATION_README.md       # Guía detallada de integración con TSLib
├── QUICK_START.md
└── test_*.py                   # Tests de integración y utilidades
```

## Imputación y Valores Faltantes

- **Validación**: En la carga, `TSLibService.validate_data()` usa TSLib `DataValidator` y además reporta cantidad y porcentaje de NaN. Si hay demasiados faltantes (según `max_missing_ratio` de TSLib), la validación puede fallar.
- **Antes de ajustar modelo**: En `services/tslib_service.py`, en `fit_model()`, `get_exploratory_analysis()` y donde se llama a TSLib con la serie, se aplica **forward fill** (ffill) a la copia de la serie si hay NaN, para que el modelo reciba una serie sin faltantes. Los diagnósticos y métricas se calculan sobre esa serie ya imputada.
- **Visualización**: En `app.py`, para graficar series con NaN se usa interpolación o `fillna(0)` según el contexto, solo con fines de plotting.

La librería TSLib no acepta NaN en el ajuste; por eso la app siempre pasa datos ya limpiados (ffill) a `model.fit()`. Para otros métodos (interpolate, drop) se puede usar `DataValidator.clean_data()` de TSLib en código propio.

## Procesos Matemáticos (vía TSLib)

Todos los modelos y la estadística se ejecutan en **time-series-library**:

- **AR(p), MA(q), ARMA(p,q), ARIMA(p,d,q)**: implementados desde cero (MLE, innovation algorithm donde aplica). Selección de orden: PACF (AR), ACF (MA), grid AIC/BIC (ARMA), ADF/KPSS + selección ARMA (ARIMA).
- **ACF/PACF**: cálculo para identificación de orden y diagnósticos de residuos.
- **Estacionariedad**: tests ADF y KPSS.
- **Métricas**: AIC, BIC, RMSE, MAE, MAPE; diagnósticos de residuos (p. ej. Ljung-Box).

Referencia matemática: en el repo **time-series-library**, `docs/mathematical_foundations.md` y `docs/modelos/` (AR, MA, ARMA, ARIMA).

## Integración con TSLib

- **Dependencia**: Este proyecto **depende** de **time-series-library** (el otro repositorio). No al revés.
- **Instalación**: En el entorno de la app, instalar la librería en modo editable, por ejemplo:
  `pip install -e /ruta/a/time-series-library`
- **Uso en código**: Toda la interacción con TSLib pasa por `services/tslib_service.py`: validación, detección de columnas fecha/valor, conversión numérica, `fit_model()`, pronósticos, análisis exploratorio (ACF/PACF), métricas. En `app.py` solo se usa directamente `ACFCalculator` para el gráfico de ACF de residuos; el resto es vía `TSLibService`.
- **Spark/ARIMA paralelo**: La app puede usar `ParallelARIMAWorkflow` de TSLib si PySpark y Java están disponibles; si no, se ofrece un flujo alternativo (p. ej. dummy/lineal). Ver `tslib_service.py` y documentación de TSLib.

Documentación detallada de pasos de uso y estado: `INTEGRATION_README.md` y `QUICK_START.md`.

## Comandos de Desarrollo

```bash
make install    # Instalar dependencias (crea venv si no existe)
make run       # Ejecutar app (requiere venv activo o make install previo)
make clean     # Limpiar archivos temporales
make clean-all # Incluye eliminar entorno virtual
make format    # Formatear código
make help      # Ayuda
```

## Tecnologías

- **Shiny for Python**: UI reactiva.
- **TSLib** (time-series-library): modelos, validación, ACF/PACF, Spark opcional.
- **Pandas, NumPy, Matplotlib (Agg), Plotly, openpyxl**: datos y gráficos.

## Licencia

MIT. Ver `LICENSE` si aplica.

## Resumen del Proyecto de Titulación

- **time-series-library**: librería de series de tiempo (AR/MA/ARMA/ARIMA desde cero, validación, imputación opcional, paralelización con PySpark).
- **tslib-shiny-app**: interfaz web que consume esa librería para un flujo completo de análisis. Ambos repositorios se analizan y mantienen como un solo proyecto de titulación; la integración es unidireccional: app → TSLib.
