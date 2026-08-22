from fastapi import FastAPI

from app.routers.molecules import router as molecules_router

app = FastAPI(
    title="Chemistry Service",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "chemistry",
    }

app.include_router(molecules_router)