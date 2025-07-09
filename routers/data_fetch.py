from fastapi import APIRouter, Query
from sqlalchemy.orm import Session
from database import SessionLocal
from models import QCCheck, User, Product, Machine
from datetime import datetime
from typing import List, Optional

router = APIRouter()

@router.get("/qc/logs")
def get_qc_logs(
    from_date: Optional[datetime] = Query(None),
    to_date: Optional[datetime] = Query(None),
    user_id: Optional[str] = Query(None),
    machine_id: Optional[str] = Query(None),
    product_id: Optional[str] = Query(None),
):
    db: Session = SessionLocal()

    query = db.query(QCCheck).join(User).join(Machine).join(Product)

    if from_date:
        query = query.filter(QCCheck.timestamp >= from_date)
    if to_date:
        query = query.filter(QCCheck.timestamp <= to_date)
    if user_id:
        query = query.filter(QCCheck.user_id == user_id)
    if machine_id:
        query = query.filter(QCCheck.machine_id == machine_id)
    if product_id:
        query = query.filter(QCCheck.product_id == product_id)

    query = query.order_by(QCCheck.timestamp.desc())
    results = query.all()

    output = []
    for check in results:
        output.append({
            "timestamp": check.timestamp.isoformat(),
            "user": check.user.name,
            "machine": check.machine.name,
            "product": check.product.name,
            "image_url": f"/uploads/{check.image_path.split('/')[-1]}"
        })

    return output

@router.get("/products")
def get_products():
    db: Session = SessionLocal()
    products = db.query(Product).all()
    return [{"id": p.id, "name": p.name} for p in products]

@router.get("/machines")
def get_machines():
    db: Session = SessionLocal()
    machines = db.query(Machine).all()
    return [{"id": m.id, "name": m.name} for m in machines]

@router.get("/users")
def get_users(role: str = Query(None)):
    db: Session = SessionLocal()
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    users = query.all()
    return [{"id": u.id, "name": u.name} for u in users]