from fastapi import FastAPI


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