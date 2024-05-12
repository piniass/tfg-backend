from config.db import conn
from models.entrenador import entrenadores
from schemas.entrenadores import Entrenador
from fastapi import HTTPException
from fastapi import Depends, Form, HTTPException, APIRouter
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi import Request
from fastapi.responses import JSONResponse
from jose import jwt, JWTError




entrenador = APIRouter()


@entrenador.get("/entrenadores")
def get_entrenadores():
    query = conn.execute(entrenadores.select())
    entrenadores_list = []
    for row in query.fetchall():
        entrenador_dict = {
            "id": row[0],
            "nombre": row[1],
            "apellido": row[2],
            "correo": row[3],
            "password": row[4],
            "avatar": row[5]
        }
        entrenadores_list.append(entrenador_dict)
    return entrenadores_list
@entrenador.get("/entrenadores/{id}")
async def get_entrenadores_byid(id:str):
    query = conn.execute(entrenadores.select().where(entrenadores.c.id == id))
    entrenadores_list = []
    for row in query:
        entrenador_dict = {
            "id": row[0],
            "nombre": row[1],
            "apellido": row[2],
            "correo": row[3],
            "password": row[4],
            "avatar": row[5]
        }
        entrenadores_list.append(entrenador_dict)
    return entrenadores_list

@entrenador.post("/entrenadores")
async def create_entrenador(
    nombre: str = Form(...),
    apellido: str = Form(...),
    correo: str = Form(...),
    password: str = Form(...),
    avatar: str = Form(...)
):
    try:
        if not nombre:
            raise HTTPException(status_code=422, detail="El campo 'nombre' está vacío")
        if not apellido:
            raise HTTPException(status_code=422, detail="El campo 'apellido' está vacío")
        if not correo:
            raise HTTPException(status_code=422, detail="El campo 'correo' está vacío")
        if not password:
            raise HTTPException(status_code=422, detail="El campo 'password' está vacío")
        if not avatar:
            raise HTTPException(status_code=422, detail="El campo 'avatar' está vacío")
    ##Controlar que los usuarios no tengan el mismo correo electronico
        new_entrenador = {
            "nombre": nombre,
            "apellido": apellido,
            "correo": correo,
            "password": password,
            "avatar": avatar
        }

        conn.execute(entrenadores.insert().values(new_entrenador))
        conn.commit()
        return {"message": f"Entrenador {nombre} {apellido} creado"}
    except HTTPException as e:
        return e.detail



@entrenador.put("/entrenadores/{id}")
async def update_entrenador(id: str, entrenador_data: Entrenador):
    updated_entrenador = {
        "nombre": entrenador_data.nombre,
        "apellido": entrenador_data.apellido,
        "correo": entrenador_data.correo,
        "password": entrenador_data.password,
        "avatar": entrenador_data.avatar
    }
    result = conn.execute(entrenadores.update().where(entrenadores.c.id == id).values(updated_entrenador))
    conn.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Entrenador no encontrado")
    return {"message": f"Entrenador con ID {id} actualizado"}

@entrenador.delete("/entrenadores/{id}")
async def delete_entrenador(id: str):
    result = conn.execute(entrenadores.delete().where(entrenadores.c.id == id))
    conn.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Entrenador no encontrado")
    return {"message": f"Entrenador con ID {id} eliminado"}


SECRET_KEY = "abcd1234"
TOKEN_SECONDS_EXP = 3600 


def get_entrenador(correo: str):
    query = conn.execute(entrenadores.select().where(entrenadores.c.correo == correo))
    return query.fetchone()  # Devuelve solo una fila

def authenticate_user(entrenador: Entrenador, password: str):
    return entrenador and entrenador.password == password


def create_token(data: dict):
    print(data)
    data_token = data.copy()
    print(data_token)
    data_token["exp"] = datetime.utcnow() + timedelta(seconds=TOKEN_SECONDS_EXP)

    print(data_token)
    token_jwt = jwt.encode(data_token, key=SECRET_KEY, algorithm="HS256")
    return token_jwt

@entrenador.post("/entrenador/login")
def login(correo: str = Form(...), password: str = Form(...)):
    # Obtener el objeto entrenador de la base de datos
    entrenador = get_entrenador(correo)
    if not entrenador:
        raise Exception("No existe el usuario")  # Usamos Exception para lanzar errores
    if not authenticate_user(entrenador, password):
        raise Exception("password incorrecta")  # Usamos Exception para lanzar errores
    print(type(entrenador))
    token = create_token({'correo':correo})
    
    # Guardar el objeto entrenador en una variable

    return {"token": token, "entrenador": entrenador}  # Retornamos el token y el objeto entrenador en un diccionario

