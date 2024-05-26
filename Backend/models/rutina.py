from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from config.db import meta, engine
from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, DateTime

rutinas = Table("rutinas", meta,
                   Column("id", Integer, primary_key=True, autoincrement=True),
                   Column("nombre",String(255)),
                   Column("foto",String(255)),
                   Column("fecha_creacion", DateTime, default=func.now()),
                   Column("id_entrenador", Integer, ForeignKey('entrenadores.id', ondelete="CASCADE"))
                   )

meta.create_all(engine)