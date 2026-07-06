from fastapi import APIRouter, HTTPException
from mysql.connector import Error

from core.config import get_db_connection
from models.usuario import Usuario

router = APIRouter(prefix="/api/usuarios", tags=["usuarios"])


@router.get("")
def get_usuarios():
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM usuario")
        records = cursor.fetchall()
        usuarios = [
            {
                "id": record[0],
                "nombre": record[1],
                "apellidos": record[2],
                "email": record[3],
                "activo": record[4],
            }
            for record in records
        ]
        return {"data": usuarios}
    except Error as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    finally:
        cursor.close()
        connection.close()


@router.post("", status_code=201)
def create_usuario(usuario: Usuario):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = """
            INSERT INTO usuario (id, nombre, apellidos, email, activo)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (usuario.id, usuario.nombre, usuario.apellidos, usuario.email, usuario.activo),
        )
        connection.commit()
        return {"message": "Usuario creado correctamente"}
    except Error as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    finally:
        cursor.close()
        connection.close()
