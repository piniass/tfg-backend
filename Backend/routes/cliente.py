from fastapi import APIRouter
from config.db import conn
from models.cliente import clientes  # Importa la tabla de clientes
from schemas.clientes import Cliente
from fastapi import HTTPException
from fastapi import Form
from sqlalchemy import or_



cliente = APIRouter()  # Cambia el nombre de la variable a cliente_router

@cliente.get("/clientes")
def get_clientes():
    query = conn.execute(clientes.select())
    cliente_list = []
    for row in query.fetchall():
        cliente_dict = {
           "id": row[0],
            "nombre": row[1],
            "apellido": row[2],
            "edad": row[3],
            "altura": row[4],
            "patologias": row[5],
            "avatar": row[6],
            "id_entrenador": row[7] 
        }
        cliente_list.append(cliente_dict)
    return cliente_list

@cliente.get("/clientes/{id}")
def get_cliente_byid(id:str):
    query = conn.execute(clientes.select().where(clientes.c.id == id))
    cliente_list = []
    for row in query:
        cliente_dict = {
            "id": row[0],
            "nombre": row[1],
            "apellido": row[4],
            "edad": row[5],
            "altura": row[6],
            "patologias": row[7],
            "avatar": row[3],
            "id_entrenador": row[8] 
        }
        cliente_list.append(cliente_dict)
    return cliente_list

@cliente.get("/clientes/entrenador/{id}")
def get_cliente_byentrenador(id:str):
    query = conn.execute(clientes.select().where(clientes.c.id_entrenador == id))
    cliente_list = []
    for row in query:
        cliente_dict = {
            "id": row[0],
            "nombre": row[1],
            "apellido": row[2],
            "edad": row[3],
            "altura": row[4],
            "patologias": row[5],
            "avatar": row[6],
            "id_entrenador": row[7],
            "id_rutina": row[8]
        }
        cliente_list.append(cliente_dict)
    return cliente_list

@cliente.get("/clientes/entrenador/{id}/{input}")
def get_cliente_nombre(id: str, input: str):
    # Define tu consulta sin ejecutarla todavía
    query = clientes.select().where(clientes.c.id_entrenador == id)

    # Añade la condición para que la columna "nombre" o "apellido" contenga la cadena especificada
    cadena_buscada = f"%{input}%"
    query = query.where(or_(clientes.c.nombre.ilike(cadena_buscada), clientes.c.apellido.ilike(cadena_buscada)))

    # Ejecuta la consulta y obtén los resultados
    resultados = conn.execute(query)

    # Itera sobre los resultados si es necesario
    cliente_list = []
    for row in resultados:
        cliente_dict = {
            "id": row[0],
            "nombre": row[1],
            "apellido": row[2],
            "edad": row[3],
            "altura": row[4],
            "patologias": row[5],
            "avatar": row[6],
            "id_entrenador": row[7] 
        }
        cliente_list.append(cliente_dict)

    return cliente_list


@cliente.post("/cliente")
def create_cliente(nombre: str = Form(...), apellido: str = Form(...), edad: int = Form(...), altura: float = Form(...), patologias: str = Form(...), avatar: str = Form(...),id_entrenador: int = Form(...)):
    new_cliente = {
        "nombre": nombre,
        "apellido": apellido,
        "edad": edad,
        "altura": altura,
        "patologias": patologias,
        "avatar": avatar,
        "id_entrenador": id_entrenador
    }
    conn.execute(clientes.insert().values(new_cliente))
    conn.commit()
    return {"message": f"Cliente {nombre} {apellido} creado"}

@cliente.put("/cliente/{id}")
def update_cliente(
    id: int,
    nombre: str = Form(...),
    apellido: str = Form(...),
    edad: int = Form(...),
    altura: float = Form(...),
    patologias: str = Form(...),
    avatar: str = Form(...)
):
    updated_cliente = {
        "nombre": nombre,
        "apellido": apellido,
        "edad": edad,
        "altura": altura,
        "patologias": patologias,
        "avatar": avatar
    }
    result = conn.execute(clientes.update().where(clientes.c.id == id).values(updated_cliente))
    conn.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return {"message": f"Cliente con ID {id} actualizado"}

@cliente.put("/cliente/rutina/{id}")
def add_rutina_cliente(
    id: int,
    id_rutina: int = Form(...)
):
    updated_cliente = {
        "id_rutina": id_rutina,
    }
    result = conn.execute(clientes.update().where(clientes.c.id == id).values(updated_cliente))
    conn.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return {"message": f"Rutina agregada al cliente {id} actualizado"}

@cliente.delete("/cliente/{id}")
def delete_cliente(id: str):
    result = conn.execute(clientes.delete().where(clientes.c.id == id))
    conn.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return {"message": f"Cliente con ID {id} eliminado"}