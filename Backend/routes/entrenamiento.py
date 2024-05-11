from fastapi import APIRouter, Form, HTTPException
from config.db import conn
from models.entrenamiento import entrenamientos  # Importa la tabla de sesiones
from schemas.entrenamientos import Entrenamientos  # Importa el esquema para crear sesiones

ruta_entrenamientos = APIRouter()  # Cambia el nombre de la variable a sesiones_router

@ruta_entrenamientos.get("/entrenamientos/sesion/{id}")
def get_entrenamientos_by_sesion_id(id: int):
    query = conn.execute(entrenamientos.select().where(entrenamientos.c.id_rutinas == id))
    entrenamientos_list = []
    for row in query:
        entrenamientos_dict = {
            "id": row[0],
            "nombre": row[1],
            "dia_semana":row[2],
            "fecha_creacion":row[3],
            "id_rutinas": row[4]
        }
        entrenamientos_list.append(entrenamientos_dict)
    return entrenamientos_list

@ruta_entrenamientos.post("/entrenamientos/sesion/{id}")
def create_entrenamiento_for_sesion(id:int,  nombre: str = Form(...),dia_semana: str = Form(...)):
    nuevo_entrenamiento = {
        "nombre": nombre,      
        "dia_semana":dia_semana,
        "id_rutina": id
    }
    conn.execute(entrenamientos.insert().values(nuevo_entrenamiento))
    conn.commit()
    return {"message": f"Entrenamiento creado para la sesion con ID {id}"}

@ruta_entrenamientos.put("/entrenamientos/{id}")
def update_sesion(id:int,   nombre: str = Form(...),dia_semana: str = Form(...)):
    nuevo_entrenamiento = {
        "nombre":nombre,      
        "dia_semana":dia_semana,
    }
    result = conn.execute(entrenamientos.update().where(entrenamientos.c.id == id).values(nuevo_entrenamiento))
    conn.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Entrenamiento no encontrado")
    return {"message": f"Entrenamiento con ID {id} actualizado"}

@ruta_entrenamientos.delete("/entrenamientos/{id}")
def delete_sesion(id: int):
    result = conn.execute(entrenamientos.delete().where(entrenamientos.c.id == id))
    conn.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Entrenamiento no encontrado")
    return {"message": f"Entrenamiento con ID {id} eliminado"}