from fastapi import APIRouter, Depends, Query, Body
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from database import get_db
from models import QCCheck, User, Product, Machine
from schemas import QCCheckDisplay
from datetime import datetime, timedelta
from pytz import timezone
from typing import Optional
import uuid
from fastapi import UploadFile
import csv
import codecs

router = APIRouter()
vn_tz = timezone('Asia/Ho_Chi_Minh')

def to_vn_time(dt):
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone("Asia/Ho_Chi_Minh"))
    else:
        dt = dt.astimezone(timezone("Asia/Ho_Chi_Minh"))
    return dt.isoformat()

# ========================================
# LẤY DỮ LIỆU QC (cho màn hình quản lý)
# ========================================
@router.get("/api/qc-checks", response_model=list[QCCheckDisplay])
def get_qc_checks(
    start: Optional[datetime] = Query(None),
    end: Optional[datetime] = Query(None),
    user: Optional[str] = Query(None),
    machine: Optional[str] = Query(None),
    product: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(QCCheck)

    if start:
        query = query.filter(QCCheck.timestamp >= start)
    if end:
        query = query.filter(QCCheck.timestamp <= end)
    if user:
        query = query.join(QCCheck.user).filter_by(name=user)
    if machine:
        query = query.join(QCCheck.machine).filter_by(name=machine)
    if product:
        query = query.join(QCCheck.product).filter_by(name=product)

    records = query.order_by(QCCheck.timestamp.desc()).all()

    return [
        {
            "timestamp": to_vn_time(r.timestamp),
            "user_name": r.user.name,
            "machine_name": r.machine.name,
            "product_name": r.product.name,
            "image_path": r.image_path
        } for r in records
    ]

# ========================================
# CÁC API CHO TRANG ADMIN
# ========================================

@router.post("/admin/delete-qc-data", response_class=PlainTextResponse)
def delete_qc_data(start: datetime = Body(...), end: datetime = Body(...), db: Session = Depends(get_db)):
    deleted = db.query(QCCheck).filter(QCCheck.timestamp >= start, QCCheck.timestamp <= end).delete()
    db.commit()
    return f"Đã xóa {deleted} bản ghi QC."

@router.post("/admin/add-user", response_class=PlainTextResponse)
def add_user(
    name: str = Body(...),
    password: str = Body(...),      # Chưa dùng đến trong DB hiện tại
    department: str = Body(...),    # Chưa dùng đến trong DB hiện tại
    role: str = Body(...),
    db: Session = Depends(get_db)
):
    new_user = User(id=str(uuid.uuid4()), name=name, role=role)
    db.add(new_user)
    db.commit()
    return f"Đã thêm nhân viên: {name}"

@router.post("/admin/add-product", response_class=PlainTextResponse)
def add_product(name: str = Body(...), db: Session = Depends(get_db)):
    new_product = Product(id=str(uuid.uuid4()), name=name)
    db.add(new_product)
    db.commit()
    return f"Đã thêm sản phẩm: {name}"

@router.post("/admin/add-machine", response_class=PlainTextResponse)
def add_machine(name: str = Body(...), db: Session = Depends(get_db)):
    new_machine = Machine(id=str(uuid.uuid4()), name=name)
    db.add(new_machine)
    db.commit()
    return f"Đã thêm máy: {name}"

@router.post("/admin/import-users", response_class=PlainTextResponse)
def import_users(file: UploadFile, db: Session = Depends(get_db)):
    reader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))
    count = 0
    for row in reader:
        if 'name' in row and 'role' in row:
            new_user = User(id=str(uuid.uuid4()), name=row['name'], role=row['role'])
            db.add(new_user)
            count += 1
    db.commit()
    return f"Đã import {count} nhân viên."
    
@router.post("/admin/import-products", response_class=PlainTextResponse)
def import_products(file: UploadFile, db: Session = Depends(get_db)):
    reader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))
    count = 0
    for row in reader:
        if 'name' in row:
            new_product = Product(id=str(uuid.uuid4()), name=row['name'])
            db.add(new_product)
            count += 1
    db.commit()
    return f"Đã import {count} sản phẩm."


@router.post("/admin/import-machines", response_class=PlainTextResponse)
def import_machines(file: UploadFile, db: Session = Depends(get_db)):
    reader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))
    count = 0
    for row in reader:
        if 'name' in row:
            new_machine = Machine(id=str(uuid.uuid4()), name=row['name'])
            db.add(new_machine)
            count += 1
    db.commit()
    return f"Đã import {count} máy."
