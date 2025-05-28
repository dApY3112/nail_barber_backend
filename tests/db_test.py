from app.db.session import SessionLocal
from sqlalchemy import text

def test_db_connection():
    db = SessionLocal()
    try:
        # thực hiện truy vấn đơn giản
        db.execute(text("SELECT 1"))
    finally:
        db.close()