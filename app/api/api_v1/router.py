from fastapi import APIRouter
from app.api.endpoints import auth, users, providers, services, availability, bookings, reviews, transactions

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(providers.router, prefix="/providers", tags=["providers"])
api_router.include_router(services.router, prefix="/services", tags=["services"])
api_router.include_router(availability.router, prefix="/availability", tags=["availability"])
api_router.include_router(bookings.router, prefix="/bookings", tags=["bookings"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
