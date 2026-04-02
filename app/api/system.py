from fastapi import APIRouter
from app.services.mikrotik_service import (
    connect_router,
    get_router_resources,
    get_router_health,
)
from app.config import ROUTER_HOST, ROUTER_USERNAME, ROUTER_PASSWORD, ROUTER_PORT

router = APIRouter()

# Rutas para obtener información de los recursos del router Mikrotik
@router.get("/router/system/resources")
def router_resources():
    try:
        api = connect_router(ROUTER_HOST, ROUTER_USERNAME, ROUTER_PASSWORD, ROUTER_PORT)
        return get_router_resources(api)
    except (ConnectionError, RuntimeError) as e:
        return {"error": str(e), "status": "error"}

@router.get("/router/system/identity")
def router_identity():
    """Obtiene la identidad del router Mikrotik."""
    try:
        api = connect_router(ROUTER_HOST, ROUTER_USERNAME, ROUTER_PASSWORD, ROUTER_PORT)
        identity = api.get_resource('/system/identity').get()
        return {"identity": identity[0]['name']}
    except (ConnectionError, RuntimeError) as e:
        return {"error": str(e), "status": "error"}
    
@router.get("/router/system/health")
def health_check():
    """Obtiene el estado de salud del sistema."""
    try:
        api = connect_router(ROUTER_HOST, ROUTER_USERNAME, ROUTER_PASSWORD, ROUTER_PORT)
        return get_router_health(api)
    except (ConnectionError, RuntimeError) as e:
        return {"error": str(e), "status": "error"}