from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class RouterConfig(Base):

    __tablename__ = "router_config"

    id = Column(Integer, primary_key=True, index=True)
    host = Column(String)
    username = Column(String)
    password = Column(String)
    port = Column(Integer)


class RouterResource(Base):

    __tablename__ = "router_resources"

    id = Column(Integer, primary_key=True, index=True)
    cpu_load = Column(String)
    free_memory = Column(String)
    total_memory = Column(String)
    timestamp = Column(String)