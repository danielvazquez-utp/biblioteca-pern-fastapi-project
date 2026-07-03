from fastapi import FastAPI
import mysql.connector
from models import Usuario

app = FastAPI()
db = mysql.connector.connect(
    host = "localhost",
    user = "biblioteca_user",
    password = "secreto12345",
    database = "biblioteca",
    consume_results = True
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

# Endpoints para usuarios
# Recuperar la lista de usuarios
@app.get("/api/usuarios")
def getUsuarios():
    cursor = db.cursor()
    try:
        usuarios = []
        query = "SELECT * from usuario"
        cursor.execute(query)
        records = cursor.fetchall()
        for record in records:
            usuario = {
                "id": record[0],
                "nombre": record[1],
                "apellidos": record[2],
                "email": record[3],
                "activo": record[4]
            }
            usuarios.append(usuario)
        return {
            "data" : usuarios
        }
    except Error as e:
        raise HTTPException(status_code=500, detail=e)
    finally:
        cursor.close()

@app.post("/api/usuarios")
def setUsuario( user: Usuario):
    cursor = db.cursor()
    try:
        query = f"INSERT INTO usuario VALUES ('{ user.id }', '{ user.nombre }', '{ user.apellidos }', '{ user.email }', '{ user.activo }')"
        cursor.execute(query)
        db.commit()
    except:
        print("Ocurrio un error")
    finally:
        cursor.close()