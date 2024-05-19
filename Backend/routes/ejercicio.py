from fastapi import APIRouter, Form, HTTPException
from config.db import conn
from models.ejercicio import ejercicios  # Importa la tabla de sesiones
from schemas.ejercicios import Ejercicios  # Importa el esquema para crear sesiones

ruta_ejercicios = APIRouter()  # Cambia el nombre de la variable a sesiones_router

@ruta_ejercicios.get("/ejercicios/entrenamiento/{id}")
def get_ejercicios_by_entrenamiento_id(id: int):
    query = conn.execute(ejercicios.select().where(ejercicios.c.id_entrenamiento == id))
    ejercicios_list = []
    for row in query:
        ejercicio_dict = {
            "id": row[0],
            "nombre":row[1],
            "grupo_muscular": row[2],
            "series": row[3],
            "repeticiones": row[4],
            "id_entrenamiento": row[5]
        }
        ejercicios_list.append(ejercicio_dict)
    return ejercicios_list

@ruta_ejercicios.post("/ejercicios/entreanmiento")
def create_ejercicio_for_entrenamiento(id_entrenamiento:int= Form(...), nombre: str = Form(...),grupo_muscular: str = Form(...),series:int=Form(...),repeticiones:int=Form(...)):
    nuevo_ejercicio = {
        "nombre": nombre,
        "grupo_muscular": grupo_muscular,
        "series": series,
        "repeticiones": repeticiones,
        "id_entrenamiento": id_entrenamiento
    }
    conn.execute(ejercicios.insert().values(nuevo_ejercicio))
    conn.commit()
    return {"message": f"Ejercicio creado para el entrenamiento con ID {id}"}

@ruta_ejercicios.put("/ejercicios/{id}")
def update_ejercicio(id:int,  nombre: str = Form(...),grupo_muscular: str = Form(...),series:int=Form(...),repeticiones:int=Form(...)):
    nuevo_ejercicio = {
        "nombre": nombre,
        "grupo_muscular": grupo_muscular,
        "series": series,
        "repeticiones": repeticiones,
    }
    result = conn.execute(ejercicios.update().where(ejercicios.c.id == id).values(nuevo_ejercicio))
    conn.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    return {"message": f"Ejercicio con ID {id} actualizado"}

@ruta_ejercicios.delete("/ejercicios/{id}")
def delete_ejercicio(id: int):
    result = conn.execute(ejercicios.delete().where(ejercicios.c.id == id))
    conn.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    return {"message": f"Ejercicio con ID {id} eliminado"}