# database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "postgresql://qcuser:nkpmo2025@localhost/qcdb"

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
