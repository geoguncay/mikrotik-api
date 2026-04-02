"""
Script de verificación para validar que todos los módulos se importan correctamente.
Ejecutar: python verify_imports.py
"""

import sys
import traceback

modules_to_check = [
    "app.config",
    "app.database.models",
    "app.database.db",
    "app.security.crypto",
    "app.services.mikrotik_service",
    "app.api.router",
    "app.api.resources",
    "app.api.queues",
    "app.api.addresses",
    "app.scheduler.collector",
    "app.main",
]

print("=" * 60)
print("Verificando importación de módulos...")
print("=" * 60)

all_ok = True
for module in modules_to_check:
    try:
        __import__(module)
        print(f"✅ {module}")
    except Exception as e:
        print(f"❌ {module}")
        print(f"   Error: {str(e)}")
        traceback.print_exc()
        all_ok = False

print("=" * 60)
if all_ok:
    print("✅ Todos los módulos se importan correctamente!")
    print("El proyecto está listo para ejecutarse.")
else:
    print("❌ Hay errores en la importación de módulos.")
    print("Por favor, revisa los errores anteriores.")
    sys.exit(1)
