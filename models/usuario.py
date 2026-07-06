from pydantic import BaseModel


class Usuario(BaseModel):
    id: int
    nombre: str
    apellidos: str
    email: str
    activo: bool

