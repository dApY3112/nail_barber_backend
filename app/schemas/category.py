# src/app/schemas/category.py
from pydantic import BaseModel

class CategoryResponse(BaseModel):
    id: str
    name: str

    class Config:
        orm_mode = True  # không bắt buộc vì chỉ có field đơn giản
