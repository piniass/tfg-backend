from pydantic import BaseModel
from typing import Optional

class Cliente(BaseModel):
    id: Optional[int]
    nombre: str
    apellido: str
    edad: int
    altura: float
    patologias: Optional[str]
    avatar: str
    id_entrenador: int
    id_rutina: int