import routeros_api
from typing import Any, Dict, List
from app.config import ROUTER_HOST, ROUTER_USERNAME, ROUTER_PASSWORD, ROUTER_PORT

# Conexión al router Mikrotik y obtención de la API
def connect_router(
    host: str = ROUTER_HOST,
    username: str = ROUTER_USERNAME,
    password: str = ROUTER_PASSWORD,
    port: int = ROUTER_PORT
):
    try:
        connection = routeros_api.RouterOsApiPool(
            host,
            username=username,
            password=password,
            port=port,
            plaintext_login=True
        )
        api = connection.get_api()
        return api
    except (ConnectionError, OSError) as e:
        raise ConnectionError(f"Error conectando con router {host}: {str(e)}") from e

# Obtiene los recursos del sistema del router.
def get_router_resources(api) -> Dict[str, Any]:
    try:
        resource = api.get_resource('/system/resource')
        return resource.get()
    except (AttributeError, RuntimeError) as e:
        raise RuntimeError(f"Error obteniendo recursos: {str(e)}") from e

# Obtiene el estado de salud del sistema del router.
def get_router_health(api) -> Dict[str, Any]:
    try:
        health = api.get_resource('/system/health')
        return health.get()
    except (AttributeError, RuntimeError) as e:
        raise RuntimeError(f"Error obteniendo estado de salud: {str(e)}") from e

# Obtiene la identidad del router.
def get_router_identity(api) -> Dict[str, Any]:
    try:
        identity = api.get_resource('/system/identity')
        return identity.get()
    except (AttributeError, RuntimeError) as e:
        raise RuntimeError(f"Error obteniendo identidad: {str(e)}") from e

# Obtiene las colas simples del router.
def get_simple_queues(api) -> List[Dict[str, Any]]:
    try:
        queues = api.get_resource('/queue/simple')
        return queues.get()
    except (AttributeError, RuntimeError) as e:
        raise RuntimeError(f"Error obteniendo colas: {str(e)}") from e   

# Obtiene las colas simples filtradas por cola padre.
def queues_by_parent(api, parent_name: str) -> List[Dict[str, Any]]:
    try:
        queues = api.get_resource('/queue/simple')
        all_queues = queues.get()
        # Filtrar por padre
        filtered_queues = [q for q in all_queues if q.get('parent') == parent_name]
        return filtered_queues
    except (AttributeError, RuntimeError) as e:
        raise RuntimeError(f"Error obteniendo colas por padre: {str(e)}") from e

# Obtiene las direcciones IP del router.
def get_addresses_list(api) -> List[Dict[str, Any]]:
    try:
        addresses = api.get_resource('/ip/firewall/address-list')
        return addresses.get()
    except (AttributeError, RuntimeError) as e:
        raise RuntimeError(f"Error obteniendo Address List: {str(e)}") from e


# Obtiene las reglas de mangle del router.
def get_mangle_rules(api) -> List[Dict[str, Any]]:
    try:
        mangle = api.get_resource('/ip/firewall/mangle')
        return mangle.get()
    except (AttributeError, RuntimeError) as e:
        raise RuntimeError(f"Error obteniendo reglas de mangle: {str(e)}") from e

# Obtiene PPPoE Interfaces del router.
def get_pppoe_interfaces(api) -> List[Dict[str, Any]]:
    """Obtiene las interfaces PPPoE-Server configuradas en el router."""
    try:
        pppoe = api.get_resource('/interface/pppoe-server')
        return pppoe.get()
    except (AttributeError, RuntimeError) as e:
        raise RuntimeError(f"Error obteniendo PPPoE Interfaces: {str(e)}") from e

# Obtiene secretos PPP del router (usuarios PPP).
def get_pppoe_servers(api) -> List[Dict[str, Any]]:
    """Obtiene los secretos/usuarios PPP configurados en el router."""
    try:
        ppp_secrets = api.get_resource('/ppp/secret')
        return ppp_secrets.get()
    except (AttributeError, RuntimeError) as e:
        raise RuntimeError(f"Error obteniendo secretos PPP: {str(e)}") from e

# Obtiene PPPoE Profiles del router.
def get_pppoe_profiles(api) -> List[Dict[str, Any]]:
    try:
        pppoe_profiles = api.get_resource('/ppp/profile')
        return pppoe_profiles.get()
    except (AttributeError, RuntimeError) as e:
        raise RuntimeError(f"Error obteniendo PPPoE Profiles: {str(e)}") from e

# Obtiene PPPoE Active del router.
def get_pppoe_active(api) -> List[Dict[str, Any]]:
    try:
        pppoe_active = api.get_resource('/ppp/active')
        return pppoe_active.get()
    except (AttributeError, RuntimeError) as e:
        raise RuntimeError(f"Error obteniendo PPPoE Active: {str(e)}") from e