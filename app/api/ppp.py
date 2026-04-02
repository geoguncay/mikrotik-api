from fastapi import APIRouter
from app.services.mikrotik_service import(
    connect_router,
    get_pppoe_interfaces,
    get_pppoe_servers,
    get_pppoe_profiles,
    get_pppoe_active
)

from app.config import ROUTER_HOST, ROUTER_USERNAME, ROUTER_PASSWORD, ROUTER_PORT   

router = APIRouter()

# Rutas para obtener ppp info del router Mikrotik
@router.get("/router/ppp/interfaces")
def ppp_interfaces():
    """Obtiene las interfaces PPPoE del router."""
    try:
        api = connect_router(ROUTER_HOST, ROUTER_USERNAME, ROUTER_PASSWORD, ROUTER_PORT)
        interfaces = get_pppoe_interfaces(api)
        
        # Si no hay interfaces, retorna mensaje indicativo
        if not interfaces or len(interfaces) == 0:
            return {
                "data": [],
                "message": "No hay interfaces PPPoE configuradas en el router",
                "count": 0
            }
        
        return {
            "data": interfaces,
            "count": len(interfaces)
        }
    except (ConnectionError, RuntimeError) as e:
        return {"error": str(e), "status": "error"}
    

@router.get("/router/ppp/servers")
def ppp_servers():
    """Obtiene los secretos/usuarios PPP del router."""
    try:
        api = connect_router(ROUTER_HOST, ROUTER_USERNAME, ROUTER_PASSWORD, ROUTER_PORT)
        servers = get_pppoe_servers(api)
        
        # Si no hay secretos/usuarios, retorna mensaje indicativo
        if not servers or len(servers) == 0:
            return {
                "data": [],
                "message": "No hay secretos/usuarios PPP configurados en el router",
                "count": 0
            }
        
        return {
            "data": servers,
            "count": len(servers)
        }
    except (ConnectionError, RuntimeError) as e:
        return {"error": str(e), "status": "error"}

@router.get("/router/ppp/profiles")
def ppp_profiles():
    """Obtiene los perfiles PPP del router."""
    try:
        api = connect_router(ROUTER_HOST, ROUTER_USERNAME, ROUTER_PASSWORD, ROUTER_PORT)
        profiles = get_pppoe_profiles(api)
        
        # Si no hay perfiles, retorna mensaje indicativo
        if not profiles or len(profiles) == 0:
            return {
                "data": [],
                "message": "No hay perfiles PPP configurados en el router",
                "count": 0
            }
        
        return {
            "data": profiles,
            "count": len(profiles)
        }
    except (ConnectionError, RuntimeError) as e:
        return {"error": str(e), "status": "error"}

@router.get("/router/ppp/active")
def ppp_active():
    """Obtiene las conexiones PPP activas del router."""
    try:
        api = connect_router(ROUTER_HOST, ROUTER_USERNAME, ROUTER_PASSWORD, ROUTER_PORT)
        active = get_pppoe_active(api)
        
        # Si no hay conexiones activas, retorna mensaje indicativo
        if not active or len(active) == 0:
            return {
                "data": [],
                "message": "No hay conexiones PPP activas en el router",
                "count": 0
            }
        
        return {
            "data": active,
            "count": len(active)
        }
    except (ConnectionError, RuntimeError) as e:
        return {"error": str(e), "status": "error"}