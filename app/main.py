from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from jinja2 import Environment, FileSystemLoader
from sqlalchemy.orm import Session
from pathlib import Path
from pydantic import BaseModel
from typing import Optional
from app.api import ip_firewall, queues, system, ppp
from app.database.db import init_db, get_db
from app.database.models import RouterConfig
from app.security.crypto import encrypt_password, decrypt_password
from app.scheduler.collector import start_scheduler, stop_scheduler
from app.services.mikrotik_service import connect_router, get_router_identity

app = FastAPI()

# Configurar Jinja2 directamente
BASE_DIR = Path(__file__).resolve().parent
jinja_env = Environment(loader=FileSystemLoader(str(BASE_DIR / "templates")))

# Variable global para almacenar conexión actual y estado
current_connection = {
    "connected": False,
    "api": None,
    "host": None,
    "identity": None,
    "version": None
}

# Modelos Pydantic para requests
class TestConnectionRequest(BaseModel):
    host: str
    username: str
    password: str
    port: int = 8728

# Inicializar base de datos
@app.on_event("startup")
def startup_event():
    """Evento de inicio de la aplicación."""
    init_db()
    start_scheduler()
    print("Aplicación iniciada correctamente.")


@app.on_event("shutdown")
def shutdown_event():
    """Evento de cierre de la aplicación."""
    stop_scheduler()
    print("Aplicación cerrada correctamente.")


# Incluir routers
app.include_router(system.router)
app.include_router(queues.router)
app.include_router(ip_firewall.router)
app.include_router(ppp.router)


@app.get("/")
def home():
    """Página de inicio."""
    return {"message": "Bienvenido a MK System Pro"}


@app.get("/config", response_class=HTMLResponse)
def config_page(request: Request):
    """Página de configuración."""
    try:
        template = jinja_env.get_template("config.html")
        html = template.render(request=request)
        return html
    except Exception as e:
        return f"Error cargando template: {str(e)}"


@app.post("/config")
def save_config(
    host: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    port: int = Form(...),
    db: Session = Depends(get_db)
):
    """Guarda la configuración del router en la base de datos."""
    try:
        # Encriptar la contraseña
        encrypted_password = encrypt_password(password)
        
        # Verificar si ya existe una configuración
        existing_config = db.query(RouterConfig).first()
        if existing_config:
            existing_config.host = host
            existing_config.username = username
            existing_config.password = encrypted_password
            existing_config.port = port
        else:
            new_config = RouterConfig(
                host=host,
                username=username,
                password=encrypted_password,
                port=port
            )
            db.add(new_config)
        
        db.commit()
        return {"status": "saved", "message": "Configuración guardada correctamente."}
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}


# === ENDPOINTS DE API PARA CONEXIÓN ===

@app.get("/api/connection-status")
def get_connection_status():
    """Obtiene el estado actual de conexión al router."""
    return {
        "connected": current_connection["connected"],
        "host": current_connection["host"],
        "identity": current_connection["identity"],
        "version": current_connection["version"]
    }


@app.post("/api/test-connection")
def test_connection(request: TestConnectionRequest, db: Session = Depends(get_db)):
    """Realiza un test de conexión con los parámetros proporcionados."""
    try:
        # Intentar conectar
        api = connect_router(
            host=request.host,
            username=request.username,
            password=request.password,
            port=request.port
        )
        
        # Obtener identidad del router
        try:
            identity_data = api.get_resource('/system/identity').get()
            identity = identity_data[0]['name'] if identity_data else 'Unknown'
        except:
            identity = 'Unknown'
        
        # Obtener versión
        try:
            resource_data = api.get_resource('/system/resource').get()
            version = resource_data[0]['version'] if resource_data else 'Unknown'
        except:
            version = 'Unknown'
        
        # Actualizar estado global
        current_connection["connected"] = True
        current_connection["api"] = api
        current_connection["host"] = request.host
        current_connection["identity"] = identity
        current_connection["version"] = version
        
        return {
            "success": True,
            "identity": identity,
            "version": version,
            "message": "Conexión exitosa"
        }
    except Exception as e:
        current_connection["connected"] = False
        current_connection["api"] = None
        return {
            "success": False,
            "message": str(e)
        }


@app.post("/api/disconnect")
def disconnect():
    """Desconecta del router actual."""
    try:
        current_connection["connected"] = False
        current_connection["api"] = None
        current_connection["host"] = None
        current_connection["identity"] = None
        current_connection["version"] = None
        
        return {
            "success": True,
            "message": "Desconectado correctamente"
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }


@app.get("/api/get-config")
def get_config(db: Session = Depends(get_db)):
    """Obtiene la configuración guardada del router."""
    try:
        config = db.query(RouterConfig).first()
        if config:
            return {
                "config": {
                    "host": config.host,
                    "username": config.username,
                    "port": config.port
                }
            }
        else:
            return {"config": None}
    except Exception as e:
        return {"config": None, "error": str(e)}