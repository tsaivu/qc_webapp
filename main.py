from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from database import engine, Base
from routers import qc_check, data_fetch, manage_api
from routers import manage_api


# Khởi tạo ứng dụng
app = FastAPI()

# Tạo bảng trong database
Base.metadata.create_all(bind=engine)

# Thiết lập thư mục template và static
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Gắn các router vào app
app.include_router(qc_check.router)
app.include_router(data_fetch.router)
app.include_router(manage_api.router)

# Trang chính
@app.get("/")
def read_root():
    return {"msg": "QC WebApp running"}

# Giao diện QC
@app.get("/qc")
def qc_form(request: Request):
    return templates.TemplateResponse("qc_form.html", {"request": request})

# Giao diện quản lý
@app.get("/manage")
def manage_page(request: Request):
    return templates.TemplateResponse("manage.html", {"request": request})

@app.get("/admin")
def admin_page(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})