from fastapi import APIRouter, HTTPException
from config.db import conn
from models.rutina import rutinas  # Importa la tabla de rutinas
from schemas.rutinas import Rutinas  # Importa el esquema para crear rutinas
from fastapi import Form

ruta_rutinas = APIRouter() 

@ruta_rutinas.get("/rutinas/cliente/{id}")
def get_rutinas_by_cliente_id(id: int):
    query = conn.execute(rutinas.select().where(rutinas.c.id_cliente == id))
    sesiones_list = []
    for row in query:
        rutinas_dict = {
            "id": row[0],
            "nombre": row[1],
            "foto":row[2],
            "fecha_creacion": row[3],
            "id_cliente": row[4]
        }
        sesiones_list.append(rutinas_dict)
    return sesiones_list

@ruta_rutinas.post("/rutinas/cliente/{id}")
def create_rutinas_for_cliente(id:int, nombre: str = Form(...),foto: str = Form(...)):
    nueva_rutina = {
        "nombre": nombre,
        "foto":foto,
        "id_cliente": id
    }
    conn.execute(rutinas.insert().values(nueva_rutina))
    conn.commit()
    return {"message": f"Sesión creada para el cliente con ID {id}"}

@ruta_rutinas.put("/rutinas/{id}")
def update_rutinas(id:int, nombre: str = Form(...),foto: str = Form(...)):
    nueva_rutina = {
        "nombre":nombre,
        "foto":foto,
    }
    result = conn.execute(rutinas.update().where(rutinas.c.id == id).values(nueva_rutina))
    conn.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    return {"message": f"Sesión con ID {id} actualizada"}

@ruta_rutinas.delete("/rutinas/{id}")
def delete_rutinas(id: int):
    result = conn.execute(rutinas.delete().where(rutinas.c.id == id))
    conn.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    return {"message": f"Sesión con ID {id} eliminada"}
