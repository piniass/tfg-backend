from fastapi import APIRouter, Form, HTTPException
from config.db import conn
from models.ejercicio import ejercicios  # Importa la tabla de sesiones
from schemas.ejercicios import Ejercicios  # Importa el esquema para crear sesiones
from sqlalchemy import text
import time


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
    return {"message": f"Ejercicio creado para el entrenamiento con ID {id_entrenamiento}"}

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

@ruta_ejercicios.get("/ejercicios/rutina/cliente/{id_cliente}")
def count_grupo_rutina(id_cliente: int):
    time.sleep(2)
    query = text(
        """
        SELECT grupo_muscular, COUNT(*) as total
        FROM ejercicios
        JOIN entrenamientos ON ejercicios.id_entrenamiento = entrenamientos.id
        JOIN rutinas ON entrenamientos.id_rutina = rutinas.id
        JOIN clientes ON rutinas.id = clientes.id_rutina
        WHERE clientes.id = :id_cliente
        GROUP BY grupo_muscular
        """
    )
    result = conn.execute(query, {"id_cliente": id_cliente}).fetchall()
    count = {row[0]: row[1] for row in result}
    return count
