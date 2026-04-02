from fastapi import APIRouter
from app.services.mikrotik_service import connect_router, get_simple_queues, queues_by_parent
from app.config import ROUTER_HOST, ROUTER_USERNAME, ROUTER_PASSWORD, ROUTER_PORT

router = APIRouter()

# Rutas para obtener información de las colas del router Mikrotik
@router.get("/router/queues")
def queues():
    try:
        api = connect_router(ROUTER_HOST, ROUTER_USERNAME, ROUTER_PASSWORD, ROUTER_PORT)
        queues = get_simple_queues(api)
        # Si no hay colas, retorna mensaje indicativo
        if not queues or len(queues) == 0:
            return {
                "data": [],
                "message": "No hay colas simples configuradas en el router",
                "count": 0
            }
        return {
            "data": queues,
            "count": len(queues)
        }
    except (ConnectionError, RuntimeError) as e:
        return {"error": str(e), "status": "error"}

# Ruta para listar colas padre disponibles con la información completa de cada una
@router.get("/router/queues/parent")
def list_queue_parents():
    """Obtiene la lista de colas padre disponibles en el router Mikrotik."""
    try:
        api = connect_router(ROUTER_HOST, ROUTER_USERNAME, ROUTER_PASSWORD, ROUTER_PORT)
        parents = get_simple_queues(api)
        # Si no hay colas padre, retorna mensaje indicativo
        parent_queues = [queue for queue in parents if queue.get('parent') == 'none']
        if not parent_queues or len(parent_queues) == 0:
            return {
                "data": [],
                "message": "No hay colas padre configuradas en el router",
                "count": 0
            }
        return {
            "data": parent_queues,
            "count": len(parent_queues)
        }
    except (ConnectionError, RuntimeError) as e:
        return {"error": str(e), "status": "error"}
    
# Ruta para obtener colas simples filtradas por el target de la cola
@router.get("/router/queues/filter")
def get_queues_by_filter(name: str = None, parent: str = None, target: str = None):
    """Obtiene las colas simples del router Mikrotik filtradas por nombre, padre o target.
    
    Parámetros de query (todos opcionales):
    - name: Filtrar por nombre de la cola
    - parent: Filtrar por cola padre
    - target: Filtrar por target (puede ser interfaz o IP como 192.168.20.15/32)
    
    Ejemplos:
    - /router/queues/filter?name=Clientes
    - /router/queues/filter?parent=none
    - /router/queues/filter?target=bridge1
    - /router/queues/filter?target=192.168.20.15/32
    """
    try:
        api = connect_router(ROUTER_HOST, ROUTER_USERNAME, ROUTER_PASSWORD, ROUTER_PORT)
        queues = get_simple_queues(api)
        
        # Aplicar filtros
        filtered_queues = queues
        
        if name:
            filtered_queues = [q for q in filtered_queues if q.get('name') == name]
        
        if parent:
            filtered_queues = [q for q in filtered_queues if q.get('parent') == parent]
        
        if target:
            filtered_queues = [q for q in filtered_queues if q.get('target') == target]
        
        # Si no hay colas que cumplan los filtros
        if not filtered_queues or len(filtered_queues) == 0:
            filters_text = []
            if name:
                filters_text.append(f"nombre '{name}'")
            if parent:
                filters_text.append(f"padre '{parent}'")
            if target:
                filters_text.append(f"target '{target}'")
            
            filter_str = " y ".join(filters_text) if filters_text else "los criterios especificados"
            
            return {
                "data": [],
                "message": f"No hay colas simples con {filter_str} configuradas en el router",
            }
        return {
            "data": filtered_queues,
        }
    except (ConnectionError, RuntimeError) as e:
        return {"error": str(e), "status": "error"}
