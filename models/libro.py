from pydantic import BaseModel
from typing import List, Union

class Libro(BaseModel):
    id: Union[int, None] = None
    titulo: str
    autor: str
    editorial: str
    isbn: str
    disponible: bool