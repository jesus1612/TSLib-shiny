.PHONY: install run clean clean-all format help setup-venv check-venv

# Default target
help:
	@echo "Available commands:"
	@echo "  install    - Install dependencies (creates venv if needed)"
	@echo "  run        - Run the Shiny application (requires venv)"
	@echo "  clean      - Clean cache and temporary files"
	@echo "  clean-all  - Clean everything including virtual environment"
	@echo "  format     - Format Python code with black"
	@echo "  setup-venv - Create virtual environment manually"
	@echo "  help       - Show this help message"

# Check if virtual environment exists
check-venv:
	@if [ ! -d "venv" ]; then \
		echo "Creating virtual environment..."; \
		python3 -m venv venv; \
		echo "Virtual environment created."; \
	fi

# Create virtual environment manually
setup-venv:
	python3 -m venv venv
	@echo "Virtual environment created. Run 'source venv/bin/activate' to activate it."

# Install dependencies (auto-creates venv if needed)
install: check-venv
	@echo "Installing dependencies..."
	@if [ -f "venv/bin/activate" ]; then \
		. venv/bin/activate && pip install -r requirements.txt; \
	else \
		python3 -m pip install -r requirements.txt; \
	fi
	@echo "Dependencies installed successfully!"

# Run the application
run:
	@if [ ! -d "venv" ]; then \
		echo "❌ Error: No se encontró el entorno virtual."; \
		echo "💡 Solución: Ejecuta 'make install' primero para crear el entorno virtual e instalar las dependencias."; \
		exit 1; \
	fi
	@if [ ! -f "venv/bin/activate" ]; then \
		echo "❌ Error: El entorno virtual está corrupto."; \
		echo "💡 Solución: Ejecuta 'make clean && make install' para recrear el entorno."; \
		exit 1; \
	fi
	@echo "✅ Ejecutando aplicación con entorno virtual..."
	. venv/bin/activate && python app.py

# Clean cache and temporary files
clean:
	@echo "🧹 Limpiando archivos temporales..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@echo "✅ Limpieza completada."

# Clean everything including virtual environment
clean-all: clean
	@echo "🗑️ Eliminando entorno virtual..."
	rm -rf venv
	@echo "✅ Entorno virtual eliminado."

# Format code
format:
	black . --line-length 88
