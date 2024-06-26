from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey  # Importa ForeignKey de sqlalchemy
from config.db import meta, engine

clientes = Table(
    "clientes", meta,
    Column("id", Integer, primary_key=True),
    Column("nombre", String(100), nullable=True),
    Column("apellido", String(100), nullable=True),
    Column("edad", Integer, nullable=True),
    Column("altura", Float, nullable=True),
    Column("patologias", String(255), nullable=True),
    Column("avatar", String(100), nullable=True),
    Column("id_entrenador", Integer, ForeignKey("entrenadores.id"), nullable=True),
    Column("id_rutina", Integer, ForeignKey("rutinas.id", ondelete="SET NULL"), nullable=True)
)

