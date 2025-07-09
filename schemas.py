# schemas.py
from pydantic import BaseModel
from datetime import datetime

class QCCheckDisplay(BaseModel):
    timestamp: datetime
    user_name: str
    machine_name: str
    product_name: str
    image_path: str

    class Config:
        from_attributes = True
class ProductCreate(BaseModel):
    name: str

class MachineCreate(BaseModel):
    name: str
