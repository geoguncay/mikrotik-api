#!/bin/bash

# Script para ejecutar la aplicación MK System Pro

echo "================================================"
echo "Iniciando MK System Pro"
echo "================================================"

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt

# Verificar si existe .env
if [ ! -f ".env" ]; then
    echo "Copiando .env.example a .env..."
    cp .env.example .env
    echo "Por favor, actualiza el archivo .env con tus credenciales."
    echo "Luego ejecuta este script nuevamente."
    exit 1
fi

# Iniciar la aplicación
echo "Iniciando servidor..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
