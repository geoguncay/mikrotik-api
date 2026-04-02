import os
from dotenv import load_dotenv

load_dotenv()
# Configuración del router y base de datos obtenida de variables de entorno o .env
ROUTER_HOST = os.getenv("ROUTER_HOST")
ROUTER_USERNAME = os.getenv("ROUTER_USERNAME")
ROUTER_PASSWORD = os.getenv("ROUTER_PASSWORD")
ROUTER_PORT = int(os.getenv("ROUTER_PORT"))
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.sqlite")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

if not ENCRYPTION_KEY:
    from cryptography.fernet import Fernet
    ENCRYPTION_KEY = Fernet.generate_key().decode()
    print(f"Generated new ENCRYPTION_KEY: {ENCRYPTION_KEY}")
    print("Please save this key in your .env file!")
