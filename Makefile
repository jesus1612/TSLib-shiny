# TSLib Shiny App - Makefile
# Automatización de tareas comunes para desarrollo y despliegue

.PHONY: help install setup run dev clean test lint format check-deps install-deps

# Variables
PYTHON := python3
PIP := pip3
VENV := venv
VENV_BIN := $(VENV)/bin
VENV_PYTHON := $(VENV_BIN)/python
VENV_PIP := $(VENV_BIN)/pip
APP_PORT := 8000
APP_HOST := 0.0.0.0

# Colores para output
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
NC := \033[0m # No Color

# Help target - muestra todas las opciones disponibles
help:
	@echo "$(GREEN)TSLib Shiny App - Comandos disponibles:$(NC)"
	@echo ""
	@echo "$(YELLOW)Configuración inicial:$(NC)"
	@echo "  setup          - Configuración completa del proyecto (primera vez)"
	@echo "  install        - Instala dependencias en el entorno virtual"
	@echo "  install-deps   - Instala dependencias del sistema (solo macOS)"
	@echo ""
	@echo "$(YELLOW)Desarrollo:$(NC)"
	@echo "  run            - Ejecuta la aplicación en modo producción"
	@echo "  dev            - Ejecuta la aplicación en modo desarrollo"
	@echo "  clean          - Limpia archivos temporales y cache"
	@echo ""
	@echo "$(YELLOW)Calidad de código:$(NC)"
	@echo "  test           - Ejecuta tests (cuando estén implementados)"
	@echo "  lint           - Verifica estilo de código con flake8"
	@echo "  format         - Formatea código con black"
	@echo "  check-deps     - Verifica que todas las dependencias estén instaladas"
	@echo ""
	@echo "$(YELLOW)Utilidades:$(NC)"
	@echo "  status         - Muestra estado del proyecto"
	@echo "  logs           - Muestra logs de la aplicación"
	@echo "  stop           - Detiene la aplicación si está corriendo"
	@echo ""
	@echo "$(GREEN)Ejemplo de uso:$(NC)"
	@echo "  make setup     # Primera vez"
	@echo "  make dev       # Desarrollo"
	@echo "  make run       # Producción"

# Configuración inicial completa
setup: check-python create-venv install-deps install
	@echo "$(GREEN)✅ Configuración completa!$(NC)"
	@echo "$(YELLOW)Para ejecutar la app: make dev$(NC)"

# Verificar que Python esté instalado
check-python:
	@echo "$(YELLOW)🔍 Verificando Python...$(NC)"
	@which $(PYTHON) > /dev/null || (echo "$(RED)❌ Python3 no encontrado. Instala Python 3.9+$(NC)" && exit 1)
	@$(PYTHON) --version
	@echo "$(GREEN)✅ Python OK$(NC)"

# Crear entorno virtual
create-venv:
	@echo "$(YELLOW)📦 Creando entorno virtual...$(NC)"
	@if [ ! -d "$(VENV)" ]; then \
		$(PYTHON) -m venv $(VENV); \
		echo "$(GREEN)✅ Entorno virtual creado$(NC)"; \
	else \
		echo "$(GREEN)✅ Entorno virtual ya existe$(NC)"; \
	fi

# Instalar dependencias del sistema (macOS)
install-deps:
	@echo "$(YELLOW)📋 Verificando dependencias del sistema...$(NC)"
	@if command -v brew > /dev/null; then \
		echo "$(GREEN)✅ Homebrew encontrado$(NC)"; \
		if ! command -v java > /dev/null; then \
			echo "$(YELLOW)☕ Instalando Java 17...$(NC)"; \
			brew install openjdk@17; \
		else \
			echo "$(GREEN)✅ Java ya instalado$(NC)"; \
		fi; \
	else \
		echo "$(YELLOW)⚠️  Homebrew no encontrado. Instala manualmente Java 17+$(NC)"; \
	fi

# Instalar dependencias de Python
install: create-venv
	@echo "$(YELLOW)📦 Instalando dependencias de Python...$(NC)"
	@$(VENV_PIP) install --upgrade pip
	@$(VENV_PIP) install -r requirements.txt
	@echo "$(GREEN)✅ Dependencias instaladas$(NC)"

# Ejecutar en modo desarrollo
dev: check-venv
	@echo "$(GREEN)🚀 Iniciando TSLib Shiny App en modo desarrollo...$(NC)"
	@echo "$(YELLOW)📊 Abre tu navegador en: http://localhost:$(APP_PORT)$(NC)"
	@echo "$(YELLOW)⏹️  Presiona Ctrl+C para detener$(NC)"
	@$(VENV_PYTHON) app.py

# Ejecutar en modo producción
run: check-venv
	@echo "$(GREEN)🚀 Iniciando TSLib Shiny App en modo producción...$(NC)"
	@echo "$(YELLOW)📊 Abre tu navegador en: http://localhost:$(APP_PORT)$(NC)"
	@echo "$(YELLOW)⏹️  Presiona Ctrl+C para detener$(NC)"
	@$(VENV_PYTHON) app.py

# Verificar que el entorno virtual existe
check-venv:
	@if [ ! -d "$(VENV)" ]; then \
		echo "$(RED)❌ Entorno virtual no encontrado. Ejecuta: make setup$(NC)"; \
		exit 1; \
	fi
	@if [ ! -f "$(VENV_BIN)/python" ]; then \
		echo "$(RED)❌ Entorno virtual corrupto. Ejecuta: make clean && make setup$(NC)"; \
		exit 1; \
	fi

# Verificar dependencias
check-deps: check-venv
	@echo "$(YELLOW)🔍 Verificando dependencias...$(NC)"
	@$(VENV_PYTHON) -c "import shiny, pandas, numpy, plotly; print('$(GREEN)✅ Todas las dependencias están instaladas$(NC)')" || \
		(echo "$(RED)❌ Faltan dependencias. Ejecuta: make install$(NC)" && exit 1)

# Limpiar archivos temporales
clean:
	@echo "$(YELLOW)🧹 Limpiando archivos temporales...$(NC)"
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} +
	@find . -type f -name ".DS_Store" -delete
	@echo "$(GREEN)✅ Limpieza completada$(NC)"

# Limpiar completamente (incluye venv)
clean-all: clean
	@echo "$(YELLOW)🧹 Limpiando entorno virtual...$(NC)"
	@rm -rf $(VENV)
	@echo "$(GREEN)✅ Limpieza completa$(NC)"

# Formatear código
format: check-venv
	@echo "$(YELLOW)🎨 Formateando código...$(NC)"
	@$(VENV_BIN)/black . --line-length 88
	@echo "$(GREEN)✅ Código formateado$(NC)"

# Verificar estilo de código
lint: check-venv
	@echo "$(YELLOW)🔍 Verificando estilo de código...$(NC)"
	@$(VENV_BIN)/flake8 . --max-line-length=88 --ignore=E203,W503
	@echo "$(GREEN)✅ Verificación de estilo completada$(NC)"

# Ejecutar tests (cuando estén implementados)
test: check-venv
	@echo "$(YELLOW)🧪 Ejecutando tests...$(NC)"
	@if [ -d "tests" ]; then \
		$(VENV_BIN)/pytest tests/ -v; \
	else \
		echo "$(YELLOW)⚠️  No hay tests implementados aún$(NC)"; \
	fi

# Mostrar estado del proyecto
status:
	@echo "$(GREEN)📊 Estado del proyecto TSLib Shiny App:$(NC)"
	@echo ""
	@echo "$(YELLOW)Python:$(NC)"
	@$(PYTHON) --version 2>/dev/null || echo "$(RED)❌ Python no encontrado$(NC)"
	@echo ""
	@echo "$(YELLOW)Entorno virtual:$(NC)"
	@if [ -d "$(VENV)" ]; then \
		echo "$(GREEN)✅ Existe$(NC)"; \
		echo "   Ubicación: $(PWD)/$(VENV)"; \
		echo "   Python: $$($(VENV_PYTHON) --version 2>/dev/null || echo 'No disponible')"; \
	else \
		echo "$(RED)❌ No existe$(NC)"; \
	fi
	@echo ""
	@echo "$(YELLOW)Dependencias:$(NC)"
	@if [ -f "$(VENV_BIN)/python" ]; then \
		$(VENV_PYTHON) -c "import shiny, pandas, numpy, plotly; print('$(GREEN)✅ Todas instaladas$(NC)')" 2>/dev/null || echo "$(RED)❌ Faltan dependencias$(NC)"; \
	else \
		echo "$(RED)❌ Entorno virtual no disponible$(NC)"; \
	fi
	@echo ""
	@echo "$(YELLOW)Archivos del proyecto:$(NC)"
	@echo "   📁 Estructura: $$(find . -type d -name 'ui' -o -name 'server' -o -name 'utils' -o -name 'data' -o -name 'static' | wc -l) directorios principales"
	@echo "   📄 Archivos Python: $$(find . -name '*.py' | wc -l) archivos"
	@echo "   📊 Datos ejemplo: $$(find data/examples -name '*.csv' 2>/dev/null | wc -l) archivos CSV"

# Mostrar logs (si la app está corriendo)
logs:
	@echo "$(YELLOW)📋 Logs de la aplicación:$(NC)"
	@if pgrep -f "python.*app.py" > /dev/null; then \
		echo "$(GREEN)✅ Aplicación corriendo$(NC)"; \
		echo "$(YELLOW)Para ver logs en tiempo real, ejecuta la app con: make dev$(NC)"; \
	else \
		echo "$(RED)❌ Aplicación no está corriendo$(NC)"; \
		echo "$(YELLOW)Para iniciar: make dev$(NC)"; \
	fi

# Detener aplicación
stop:
	@echo "$(YELLOW)⏹️  Deteniendo aplicación...$(NC)"
	@pkill -f "python.*app.py" 2>/dev/null && echo "$(GREEN)✅ Aplicación detenida$(NC)" || echo "$(YELLOW)⚠️  No hay aplicación corriendo$(NC)"

# Instalar herramientas de desarrollo
install-dev: install
	@echo "$(YELLOW)🛠️  Instalando herramientas de desarrollo...$(NC)"
	@$(VENV_PIP) install black flake8 pytest
	@echo "$(GREEN)✅ Herramientas de desarrollo instaladas$(NC)"

# Actualizar dependencias
update-deps: check-venv
	@echo "$(YELLOW)🔄 Actualizando dependencias...$(NC)"
	@$(VENV_PIP) install --upgrade -r requirements.txt
	@echo "$(GREEN)✅ Dependencias actualizadas$(NC)"

# Crear backup del proyecto
backup:
	@echo "$(YELLOW)💾 Creando backup del proyecto...$(NC)"
	@tar -czf "tslib-shiny-app-backup-$$(date +%Y%m%d-%H%M%S).tar.gz" \
		--exclude="$(VENV)" \
		--exclude="__pycache__" \
		--exclude="*.pyc" \
		--exclude=".DS_Store" \
		.
	@echo "$(GREEN)✅ Backup creado$(NC)"

# Target por defecto
.DEFAULT_GOAL := help
