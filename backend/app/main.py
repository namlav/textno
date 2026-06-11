# main.py - Điểm khởi đầu của backend FastAPI
#
# Kỹ thuật:
# - Sử dụng FastAPI framework để xây dựng RESTful API
# - CORS middleware cho phép frontend (Streamlit) gọi API từ domain khác
# - On-shutdown event đóng kết nối MongoDB an toàn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI(
    title="Text Document Management System",
    description="Hệ thống quản lý và tìm kiếm tài liệu văn bản phi cấu trúc",
    version="1.0.0",
)

# Cho phép tất cả origin để frontend Streamlit ở cổng 8501 có thể gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.on_event("shutdown")
def shutdown():
    # Đảm bảo giải phóng tài nguyên MongoDB khi server tắt
    from app.database.mongodb import close_connection
    close_connection()
