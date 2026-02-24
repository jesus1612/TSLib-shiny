# 🚀 Inicio Rápido - TSLib Shiny App

## Instalación en 3 Pasos

```bash
# 1. Activar entorno virtual
cd /path/to/tslib-shiny-app
source venv/bin/activate

# 2. Instalar TSLib (ajusta la ruta a tu clon de time-series-library)
pip install -e /path/to/time-series-library

# 3. Instalar dependencias faltantes
pip install openpyxl pyspark
```

## Ejecutar Aplicación

```bash
python app.py
```

Abrir navegador en: **http://localhost:8000**

## Probar Integración

```bash
python test_tslib_integration.py
```

## Flujo Básico de Uso

1. **📁 Subir Archivo** → CSV o Excel
2. **🎯 Seleccionar Columna** → Valores de serie temporal
3. **✅ Validar Datos** → Click en "Validar Datos"
4. **➡️ Siguiente** → Ir a Visualización
5. **📊 Ver Gráficos** → Serie temporal, ACF, PACF
6. **➡️ Siguiente** → Ir a Selección de Modelo
7. **🤖 Elegir Modelo** → AR, MA, ARMA o ARIMA
8. **⚙️ Configurar** → Auto-selección o manual
9. **➡️ Siguiente** → Ir a Ejecución
10. **▶️ Iniciar Análisis** → Ajustar modelo
11. **➡️ Siguiente** → Ir a Resultados
12. **📈 Ver Resultados** → Métricas, pronóstico, diagnósticos

## Datos de Ejemplo

Usa los archivos en `data/examples/`:
- `sales.csv` - Datos de ventas
- `temperature.csv` - Datos de temperatura

## Modelos Disponibles

| Modelo | Mejor Para | Auto-Selección |
|--------|-----------|----------------|
| **AR** | Series con persistencia | ✅ Sí |
| **MA** | Shocks transitorios | ✅ Sí |
| **ARMA** | Estructuras complejas | ✅ Sí |
| **ARIMA** | Series con tendencia | ✅ Sí |

## Solución de Problemas

### Error: ModuleNotFoundError: No module named 'tslib'
```bash
pip install -e /path/to/time-series-library
```

### Error: ModuleNotFoundError: No module named 'openpyxl'
```bash
pip install openpyxl
```

### Error: ModuleNotFoundError: No module named 'pyspark'
```bash
pip install pyspark
```

### La validación falla
- Verifica que tienes al menos 30 observaciones
- Revisa que no haya demasiados valores faltantes
- Considera usar ARIMA si los datos tienen tendencia

### Los gráficos no aparecen
- Espera unos segundos después de cambiar de paso
- Verifica que seleccionaste una columna de valores
- Asegúrate de haber validado los datos primero

## Documentación Completa

- **`INTEGRATION_README.md`** - Guía detallada de uso
- **`IMPLEMENTATION_SUMMARY.md`** - Resumen técnico de la implementación
- **TSLib README** - Ver `README.md` en el repositorio time-series-library

## Características Principales

✅ Carga CSV y Excel  
✅ Validación automática con TSLib  
✅ 4 modelos de series temporales  
✅ Auto-selección de parámetros  
✅ Gráficos interactivos  
✅ Intervalos de confianza  
✅ Diagnósticos completos  
✅ Exportación de resultados  

## Contacto y Soporte

Para problemas o preguntas:
1. Revisar `INTEGRATION_README.md`
2. Ejecutar `test_tslib_integration.py`
3. Verificar logs en terminal
4. Consultar documentación de TSLib

---

**¡Listo para analizar series temporales! 🎉**

