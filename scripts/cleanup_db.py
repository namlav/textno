import sys
import os

# Nạp đường dẫn để gọi được module cấu hình của backend
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.database.mongodb import get_collection


def delete_old_documents(limit: int = 5000):
    collection = get_collection()

    print(f"Đang tìm {limit} tài liệu cũ nhất...")
    # 1. Tìm ID của 10.000 bài viết cũ nhất (sắp xếp tăng dần theo thời gian tạo)
    # Lọc chỉ lấy trường _id để tối ưu RAM
    # cursor = collection.find({}, {"_id": 1}).sort("created_at", 1).limit(limit)
    # Bổ sung .allow_disk_use(True) để tránh lỗi tràn bộ nhớ RAM 32MB
    cursor = (
        collection.find({}, {"_id": 1})
        .sort("created_at", 1)
        .allow_disk_use(True)
        .limit(limit)
    )

    doc_ids_to_delete = [doc["_id"] for doc in cursor]

    if not doc_ids_to_delete:
        print("Không tìm thấy tài liệu nào để xóa.")
        return

    print(f"Bắt đầu xóa {len(doc_ids_to_delete)} tài liệu...")

    # 2. Thực hiện xóa hàng loạt dựa trên danh sách ID vừa lấy
    result = collection.delete_many({"_id": {"$in": doc_ids_to_delete}})

    print(f"Hoàn tất! Đã xóa thành công {result.deleted_count} tài liệu.")


if __name__ == "__main__":
    # Bạn có thể đổi số 5000 thành số lượng bạn muốn xóa
    delete_old_documents(5000)
