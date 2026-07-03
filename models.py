from pydantic import BaseModel
from typing import Union, List

class Usuario( BaseModel ):
    id: int
    nombre: str 
    apellidos: str
    email: str
    activo: bool