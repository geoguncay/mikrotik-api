@echo off
REM Script para ejecutar la aplicación MK System Pro en Windows

echo ================================================
echo Iniciando MK System Pro
echo ================================================

REM Verificar si existe el entorno virtual
if not exist "venv" (
    echo Creando entorno virtual...
    python -m venv venv
)

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Instalar dependencias
echo Instalando dependencias...
pip install -r requirements.txt

REM Verificar si existe .env
if not exist ".env" (
    echo Copiando .env.example a .env...
    copy .env.example .env
    echo Por favor, actualiza el archivo .env con tus credenciales.
    echo Luego ejecuta este script nuevamente.
    pause
    exit /b 1
)

REM Iniciar la aplicación
echo Iniciando servidor...
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
