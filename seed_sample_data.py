from database import SessionLocal
from models import User, Product, Machine
import uuid

def gen_id():
    return str(uuid.uuid4())

def seed():
    db = SessionLocal()

    # Xóa sạch dữ liệu cũ nếu cần:
    db.query(User).delete()
    db.query(Product).delete()
    db.query(Machine).delete()

    # Người dùng
    users = [
        User(id=gen_id(), name="Nguyễn Văn A", role="congnhan"),
        User(id=gen_id(), name="Trần Thị B", role="congnhan"),
        User(id=gen_id(), name="Lê Văn C", role="congnhan")
    ]

    # Sản phẩm
    products = [
        Product(id=gen_id(), name="Túi HD 40x60"),
        Product(id=gen_id(), name="Túi PE đục quai"),
        Product(id=gen_id(), name="Túi Bio compost")
    ]

    # Máy
    machines = [
        Machine(id=gen_id(), name="Máy cắt 01"),
        Machine(id=gen_id(), name="Máy thổi 02"),
        Machine(id=gen_id(), name="Máy trộn 03")
    ]

    db.add_all(users + products + machines)
    db.commit()
    db.close()
    print("✅ Dữ liệu mẫu đã được thêm.")

if __name__ == "__main__":
    seed()
