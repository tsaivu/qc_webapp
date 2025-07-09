# database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "postgresql://qc_db_a4vr_user:brgQuurkOfhlbWrUsqyVmN25K1NL6DxY@dpg-d1mspibe5dus7382iuu0-a.oregon-postgres.render.com/qc_db_a4vr"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# 🟩 Thêm đoạn này vào cuối file:
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
