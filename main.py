from fastapi import FastAPI

from api.router import router as api_router

app = FastAPI(title="Biblioteca API")
app.include_router(api_router)


@app.get("/")
def read_root():
    return {"message": "API de biblioteca funcionando"}
