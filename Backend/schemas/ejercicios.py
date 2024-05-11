from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Ejercicios(BaseModel):
    id: Optional[int]
    nombre: str
    grupo_muscular:str
    series:int
    repeticiones:int
    id_entrenamiento: int
