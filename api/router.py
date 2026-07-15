from fastapi import APIRouter

from api.endpoints.libros import router as libro_router
from api.endpoints.usuarios import router as usuario_router

router = APIRouter()
router.include_router(libro_router)
router.include_router(usuario_router)
