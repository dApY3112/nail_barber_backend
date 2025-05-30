from fastapi import FastAPI
from app.api.api_v1.router import api_router
from app.db.session import engine
from app.models.base import Base
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Nail&Barber API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://nail-barber-rhfyx7pw7-dapys-projects.vercel.app/"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix="/api/v1")
Base.metadata.create_all(bind=engine)