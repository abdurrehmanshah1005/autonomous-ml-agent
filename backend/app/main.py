from fastapi import FastAPI
from sqlalchemy import text

from app.core.database import engine

from app.routers.projects import router as projects_router
from app.routers.datasets import router as datasets_router

app = FastAPI(
    title="Autonomous ML Agent",
    version="0.1.0",
)

app.include_router(projects_router)
app.include_router(datasets_router)


@app.get("/")
def root():
    return {
        "name": "Autonomous ML Agent",
        "status": "running",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/health/database")
def database_health():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return {
            "database": result.scalar() == 1
        }