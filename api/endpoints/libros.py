from fastapi import APIRouter, HTTPException
from mysql.connector import Error

from core.config import get_db_connection
from models.libro import Libro

router = APIRouter(prefix="/api/libros", tags=["libros"])


def _map_libro_record(record):
    return {
        "id": record[0],
        "titulo": record[1],
        "autor": record[2],
        "editorial": record[3],
        "isbn": record[4],
        "disponible": bool(record[5]),
    }


@router.get("")
def get_libros(
    titulo: str | None = None,
    autor: str | None = None,
    editorial: str | None = None,
    isbn: str | None = None,
    disponible: bool | None = None,
):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = "SELECT id, titulo, autor, editorial, isbn, disponible FROM libro"
        filters = []
        params = []

        if titulo is not None:
            filters.append("titulo LIKE %s")
            params.append(f"%{titulo}%")
        if autor is not None:
            filters.append("autor LIKE %s")
            params.append(f"%{autor}%")
        if editorial is not None:
            filters.append("editorial LIKE %s")
            params.append(f"%{editorial}%")
        if isbn is not None:
            filters.append("isbn = %s")
            params.append(isbn)
        if disponible is not None:
            filters.append("disponible = %s")
            params.append(int(disponible))

        if filters:
            query += " WHERE " + " AND ".join(filters)

        cursor.execute(query, tuple(params))
        records = cursor.fetchall()
        libros = [_map_libro_record(record) for record in records]
        return {"data": libros}
    except Error as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    finally:
        cursor.close()
        connection.close()

@router.get("/editoriales")
def get_editoriales():
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT DISTINCT editorial FROM libro WHERE editorial IS NOT NULL")
        records = cursor.fetchall()
        editoriales = [record[0] for record in records]
        return {"data": editoriales}
    except Error as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    finally:
        cursor.close()
        connection.close()

@router.post("", status_code=201)
def create_libro(libro: Libro):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = "INSERT INTO libro (titulo, autor, editorial, isbn, disponible) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (libro.titulo, libro.autor, libro.editorial, libro.isbn, int(libro.disponible)))
        connection.commit()
        return {"message": "Libro creado correctamente", "id": cursor.lastrowid}
    except Error as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    finally:
        cursor.close()
        connection.close()


@router.put("/{libro_id}")
def update_libro(libro_id: int, libro: Libro):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = f"UPDATE libro SET titulo = '{libro.titulo}', autor = '{libro.autor}', editorial = '{libro.editorial}', isbn = '{libro.isbn}', disponible = {int(libro.disponible)} WHERE id = {libro_id}"
        print(f"Executing query: {query}")  # Debugging line to print the query
        cursor.execute(query)
        connection.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Libro no encontrado")
        return {"message": "Libro actualizado correctamente"}
    except Error as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    finally:
        cursor.close()
        connection.close()


@router.delete("/{libro_id}")
def delete_libro(libro_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM libro WHERE id = %s", (libro_id,))
        connection.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Libro no encontrado")
        return {"message": "Libro eliminado correctamente"}
    except Error as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    finally:
        cursor.close()
        connection.close()


__all__ = ["router"]

