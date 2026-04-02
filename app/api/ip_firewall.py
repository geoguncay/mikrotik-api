from fastapi import APIRouter
from app.services.mikrotik_service import (
    connect_router, 
    get_addresses_list, 
    get_mangle_rules
)
from app.config import ROUTER_HOST, ROUTER_USERNAME, ROUTER_PASSWORD, ROUTER_PORT

router = APIRouter()

# Rutas para obtener la lista de direcciones del firewall y reglas de mangle del router Mikrotik
@router.get("/router/addresses_list")
def addresses():
    try:
        api = connect_router(ROUTER_HOST, ROUTER_USERNAME, ROUTER_PASSWORD, ROUTER_PORT)
        addresses_list = get_addresses_list(api)

        # Si no hay direcciones, retorna mensaje indicativo
        if not addresses or len(addresses_list) == 0:
            return {
                "data": [],
                "message": "No hay direcciones IP configuradas en el router",
                "count": 0
            }
        return {
            "data": addresses_list,
            "count": len(addresses_list)
        }
    except (ConnectionError, RuntimeError) as e:
        return {"error": str(e), "status": "error"}

# Ruta para obtener una Address List específica del router Mikrotik
@router.get("/router/addresses_list/list/{list_name}")
def addresses_list(list_name: str):
    try:
        api = connect_router(ROUTER_HOST, ROUTER_USERNAME, ROUTER_PASSWORD, ROUTER_PORT)
        addresses = get_addresses_list(api)
        filtered_addresses = [addr for addr in addresses if addr.get('list') == list_name]
        
        # Si no hay direcciones para la lista especificada, retorna mensaje indicativo
        if not filtered_addresses or len(filtered_addresses) == 0:
            return {
                "data": [],
                "message": f"No hay direcciones IP configuradas en la lista '{list_name}' del router",
                "count": 0
            }
        return {
            "data": filtered_addresses,
            "count": len(filtered_addresses)
        }
    except (ConnectionError, RuntimeError) as e:
        return {"error": str(e), "status": "error"}

# Ruta para obtener una dirección IP específica de la lista de direcciones del router Mikrotik
@router.get("/router/addresses_list/ip/{ip_address}")
def addresses_list_by_ip(ip_address: str):
    try:
        api = connect_router(ROUTER_HOST, ROUTER_USERNAME, ROUTER_PASSWORD, ROUTER_PORT)
        addresses = get_addresses_list(api)
        filtered_addresses = [addr for addr in addresses if addr.get('address') == ip_address]
        
        # Si no hay direcciones para la IP especificada, retorna mensaje indicativo
        if not filtered_addresses or len(filtered_addresses) == 0:
            return {
                "data": [],
                "message": f"No hay direcciones IP configuradas con la dirección '{ip_address}' en el router",
                "count": 0
            }
        return {
            "data": filtered_addresses,
            "count": len(filtered_addresses)
        }
    except (ConnectionError, RuntimeError) as e:
        return {"error": str(e), "status": "error"}

# Rutas para obtener las reglas de mangle del firewall del router Mikrotik
@router.get("/router/firewall/mangle")
def mangle_rules():
    try:
        api = connect_router(ROUTER_HOST, ROUTER_USERNAME, ROUTER_PASSWORD, ROUTER_PORT)
        mangle_rules = get_mangle_rules(api)
        # Si no hay reglas de mangle, retorna mensaje indicativo
        if not mangle_rules or len(mangle_rules) == 0:
            return {
                "data": [],
                "message": "No hay reglas de mangle configuradas en el router",
                "count": 0
            }
        return {
            "data": mangle_rules,
            "count": len(mangle_rules)
        }
    except (ConnectionError, RuntimeError) as e:
        return {"error": str(e), "status": "error"}
    