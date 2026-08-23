from fastapi import FastAPI
from app.routers.predictions import router as predictions_router


app = FastAPI(
    title="Prediction Service",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "prediction",
    }

app.include_router(predictions_router)