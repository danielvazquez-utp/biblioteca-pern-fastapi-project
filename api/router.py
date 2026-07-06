from fastapi import APIRouter

from api.endpoints.usuarios import router as usuario_router

router = APIRouter()
router.include_router(usuario_router)
