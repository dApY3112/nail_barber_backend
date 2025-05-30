# app/schemas/rating.py
from pydantic import BaseModel, conint

class RatingCreate(BaseModel):
    score: conint(ge=1, le=5)  # chỉ cho phép 1–5
