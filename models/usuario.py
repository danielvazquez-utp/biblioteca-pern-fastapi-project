from pydantic import BaseModel
from typing import List, Union

class Usuario(BaseModel):
    id: Union[int, None] = None
    nombre: str
    apellidos: str
    email: str
    activo: bool

