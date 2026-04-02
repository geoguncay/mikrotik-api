from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.services.mikrotik_service import connect_router, get_router_resources
from app.database.db import SessionLocal
from app.database.models import RouterResource
from app.config import ROUTER_HOST, ROUTER_USERNAME, ROUTER_PASSWORD, ROUTER_PORT
from datetime import datetime
from typing import Optional

scheduler: Optional[BackgroundScheduler] = None


def collect_data():
    """Recolecta datos del router y los guarda en la base de datos."""
    try:
        print(f"[{datetime.now()}] Recolectando datos del router...")
        api = connect_router(ROUTER_HOST, ROUTER_USERNAME, ROUTER_PASSWORD, ROUTER_PORT)
        resources = get_router_resources(api)
        
        # Guardar en base de datos
        db = SessionLocal()
        try:
            router_resource = RouterResource(
                cpu_load=str(resources[0].get('cpu-load', 'N/A')) if resources else 'N/A',
                free_memory=str(resources[0].get('free-memory', 'N/A')) if resources else 'N/A',
                total_memory=str(resources[0].get('total-memory', 'N/A')) if resources else 'N/A',
                timestamp=datetime.now().isoformat()
            )
            db.add(router_resource)
            db.commit()
            print(f"[{datetime.now()}] Datos guardados correctamente.")
        except (ValueError, AttributeError, RuntimeError) as e:
            print(f"Error guardando datos: {str(e)}")
            db.rollback()
        finally:
            db.close()
    except (ConnectionError, RuntimeError) as e:
        print(f"Error en collect_data: {str(e)}")


def start_scheduler():
    """Inicia el scheduler de background."""
    global scheduler
    if scheduler is None:
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            collect_data,
            trigger=IntervalTrigger(seconds=60),
            id='collect_data_job',
            name='Recolectar datos del router',
            replace_existing=True
        )
        scheduler.start()
        print("Scheduler iniciado correctamente.")


def stop_scheduler():
    """Detiene el scheduler de background."""
    global scheduler
    if scheduler is not None:
        scheduler.shutdown()
        scheduler = None
        print("Scheduler detenido correctamente.")