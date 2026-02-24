# TSLib Shiny App – Interfaz de Análisis de Series de Tiempo

Aplicación web interactiva (Shiny for Python) para análisis de series de tiempo. **Este repositorio es la interfaz (UI)** del proyecto de titulación; el núcleo algorítmico vive en el repositorio **time-series-library** (TSLib). La integración es unidireccional: esta app consume TSLib; TSLib no depende de esta app.

## Proyecto de titulación: dos partes en paralelo

| Repositorio | Rol | Contenido |
|-------------|-----|-----------|
| **time-series-library** | Librería (backend) | Modelos AR/MA/ARMA/ARIMA, validación, ACF/PACF, opcionalmente ARIMA paralelo con PySpark |
| **tslib-shiny-app** (este repo) | Interfaz (frontend) | Wizard de pasos, carga de datos, visualización, selección de modelo, ejecución y resultados |

La app llama a TSLib para validar datos, ajustar modelos, obtener pronósticos y métricas. Toda la interacción con TSLib se hace a través de `services/tslib_service.py`.

## Características

- **Flujo en 4 pasos**: Carga de datos → Exploración → Modelo y ejecución → Resultados.
- **Modelos**: AR, MA, ARIMA y ARMA con auto-selección de orden vía TSLib.
- **Validación**: TSLib `DataValidator`, reporte de NaN y outliers.
- **Visualización**: Serie temporal, ACF/PACF, estadísticas básicas, pronósticos e intervalos de confianza.
- **ARIMA paralelo** (opcional): Si PySpark y Java están disponibles, se usa `ParallelARIMAWorkflow` de TSLib; si no, se usa un flujo lineal de respaldo para que la app siga funcionando.
- Tema oscuro, UI en español, código organizado por features.

## Requisitos

- Python 3.8+
- **TSLib** instalado en el mismo entorno. Ver [Integración con TSLib](#integración-con-tslib).

## Instalación

```bash
git clone <url-repo-tslib-shiny-app>
cd tslib-shiny-app
make install
```

Instalar TSLib desde la ruta donde clonaste **time-series-library**:

```bash
pip install -e /ruta/absoluta/time-series-library
```

En `requirements.txt` hay una nota con la ruta; ajústala a tu máquina.

## Ejecución

```bash
make run
```

Abrir en el navegador: `http://localhost:8000`.

## Estructura del proyecto

```
tslib-shiny-app/
├── app.py                    # Entry point Shiny; estado y orquestación de pasos
├── components/
│   ├── layout.py             # Layout (sidebar, cards, tablas, formularios)
│   └── stepper.py            # Componente de pasos del wizard
├── features/
│   ├── upload/ui.py          # Carga CSV/Excel, columnas, validación
│   ├── visualization/ui.py   # Gráfico de serie, estadísticas, ACF/PACF
│   ├── model_selection/ui.py # Tipo de modelo, auto/manual, ejecución
│   ├── results/ui.py         # Métricas, pronóstico, diagnósticos, exportar
│   └── reports/ui.py         # UI de reportes (en desarrollo)
├── services/
│   └── tslib_service.py       # Capa de integración con TSLib
├── static/
│   └── styles.css
├── data/examples/
│   ├── generate_dummy_data.py
│   ├── dummy_with_missing.csv
│   ├── sales.csv
│   └── temperature.csv
├── requirements.txt
├── Makefile
├── README.md
├── INTEGRATION_README.md     # Guía detallada de integración
└── QUICK_START.md
```

## Integración con TSLib

- **Dependencia**: Este proyecto **depende** de **time-series-library**. No al revés.
- **Instalación**: En el entorno de la app:  
  `pip install -e /ruta/a/time-series-library`
- **Uso en código**: Toda la interacción con TSLib pasa por `services/tslib_service.py`: validación, columnas fecha/valor, conversión numérica, `fit_model()`, pronósticos, ACF/PACF, métricas. En `app.py` solo se usa directamente `ACFCalculator` (tslib) para el gráfico de ACF de residuos; el resto es vía `TSLibService`.
- **ARIMA paralelo**: La app usa `ParallelARIMAWorkflow` de TSLib si PySpark (y Java) están disponibles; si no, un flujo lineal de respaldo permite seguir usando ARIMA sin Spark. Ver `tslib_service.py`.

Documentación de uso y estado: `INTEGRATION_README.md` y `QUICK_START.md`.

## Imputación y valores faltantes

- **Validación**: En la carga, `TSLibService.validate_data()` usa el `DataValidator` de TSLib y reporta cantidad y porcentaje de NaN. Si hay demasiados faltantes (según `max_missing_ratio` de TSLib), la validación puede fallar.
- **Antes de ajustar**: En `fit_model()`, `get_exploratory_analysis()` y donde se llama a TSLib con la serie, se aplica relleno (forward fill / interpolación) a una copia de la serie si hay NaN, para que el modelo reciba datos sin faltantes.
- **Gráficos**: Para plotear series con NaN se usa interpolación o relleno solo con fines de visualización.

TSLib no acepta NaN en el ajuste; la app siempre pasa datos ya limpiados a `model.fit()`.

## Procesos matemáticos (vía TSLib)

Modelos y estadística se ejecutan en **time-series-library**:

- **AR(p), MA(q), ARMA(p,q), ARIMA(p,d,q)**: implementados en TSLib (MLE, algoritmo de innovaciones donde aplica). Selección de orden: PACF (AR), ACF (MA), grid AIC/BIC (ARMA), ADF/KPSS + selección ARMA (ARIMA).
- **ACF/PACF**: para identificación de orden y diagnósticos de residuos.
- **Estacionariedad**: tests ADF y KPSS.
- **Métricas**: AIC, BIC, RMSE, MAE, MAPE; diagnósticos de residuos (p. ej. Ljung-Box).

Referencia matemática: en el repo **time-series-library**, `docs/mathematical_foundations.md` y `docs/modelos/`.

## Comandos de desarrollo

```bash
make install    # Crear venv e instalar dependencias
make run        # Ejecutar app
make clean      # Limpiar temporales
make clean-all  # Incluye eliminar venv
make format     # Formatear código
make help       # Ayuda
```

## Tecnologías

- **Shiny for Python**: UI reactiva.
- **TSLib** (time-series-library): modelos, validación, ACF/PACF, Spark opcional.
- **Pandas, NumPy, Matplotlib (Agg), Plotly, openpyxl**: datos y gráficos.

## Licencia

MIT. Ver `LICENSE` si aplica.

## Resumen

- **time-series-library**: librería de series de tiempo (AR/MA/ARMA/ARIMA, validación, paralelización opcional con PySpark).
- **tslib-shiny-app**: interfaz web que consume esa librería para un flujo completo de análisis. La integración es **app → TSLib**.
