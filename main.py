from fastapi import FastAPI
from app.api.api_v1.router import api_router
from app.db.session import engine
from app.models.base import Base
app = FastAPI(title="Nail&Barber API")
app.include_router(api_router, prefix="/api/v1")
Base.metadata.create_all(bind=engine)