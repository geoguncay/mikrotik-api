from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from app.config import DATABASE_URL
from app.database.models import Base

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)


def init_db():
    """Crea todas las tablas en la base de datos."""
    Base.metadata.create_all(bind=engine)
    print("Base de datos inicializada correctamente.")


def get_db() -> Generator[Session, None, None]:
    """Retorna una sesión de base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()