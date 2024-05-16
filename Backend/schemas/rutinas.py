from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Rutinas(BaseModel):
    id: Optional[int]
    nombre: str
    foto:str
    fecha: datetime
    id_entrenador: int