from fastapi import APIRouter, UploadFile, Form, File
from sqlalchemy.orm import Session
from database import SessionLocal
from models import QCCheck
import uuid, os
from datetime import datetime, timezone, timedelta  # ✅ cập nhật

router = APIRouter()

UPLOAD_DIR = "uploads"

def save_image(file: UploadFile):
    ext = file.filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())

    return filepath

@router.post("/qc/check")
async def submit_qc_check(
    user_id: str = Form(...),
    machine_id: str = Form(...),
    product_id: str = Form(...),
    image: UploadFile = File(...)
):
    db: Session = SessionLocal()
    image_path = save_image(image)

    # ✅ Lấy giờ hiện tại theo múi giờ Việt Nam
    vn_time = datetime.now(timezone(timedelta(hours=7)))

    qc_entry = QCCheck(
        user_id=user_id,
        machine_id=machine_id,
        product_id=product_id,
        image_path=image_path,
        timestamp=vn_time
    )

    db.add(qc_entry)
    db.commit()
    db.refresh(qc_entry)

    return {"status": "success", "check_id": qc_entry.id}
