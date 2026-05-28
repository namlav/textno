# Dataset and NLP Preprocessing Report

## Nguồn dữ liệu

- Nguồn: VnExpress, dữ liệu đã crawl theo 11 chuyên mục.
- File gốc: `du-lich.json`, `giai-tri.json`, `giao-duc.json`, `khoa-hoc.json`, `kinh-doanh.json`, `phap-luat.json`, `so-hoa.json`, `suc-khoe.json`, `the-gioi.json`, `the-thao.json`, `thoi-su.json`.
- Mỗi file JSON chứa danh sách bài viết, tên file được dùng làm nhãn `category` trong dữ liệu đã xử lý.
- Tổng số bản ghi sạch sau khi loại trùng và loại bản ghi thiếu nội dung: 466 bài viết.

## Phân bố dữ liệu

| Chuyên mục | Số bài |
| --- | ---: |
| du-lich | 37 |
| giai-tri | 47 |
| giao-duc | 38 |
| khoa-hoc | 33 |
| kinh-doanh | 49 |
| phap-luat | 46 |
| so-hoa | 42 |
| suc-khoe | 50 |
| the-gioi | 47 |
| the-thao | 43 |
| thoi-su | 34 |

## Cấu trúc dữ liệu

File raw `data/raw/dataset.csv` giữ đúng format mẫu:

- `id`: mã bài viết.
- `title`: tiêu đề.
- `updatetime`: thời điểm cập nhật.
- `wordcount`: số từ theo dữ liệu crawl.
- `publication`: thời điểm xuất bản.
- `tags`: danh sách tag dạng chuỗi.
- `content`: nội dung bài viết.
- `author`: tác giả hoặc mã tác giả.

File processed `data/processed/cleaned.csv` giữ các cột trên và thêm:

- `category`: chuyên mục lấy từ tên file JSON.
- `source`: nguồn dữ liệu, hiện là `VnExpress`.
- `clean_title`: tiêu đề sau chuẩn hóa NLP.
- `clean_content`: nội dung sau chuẩn hóa NLP.
- `tokens`: token sau bước clean và remove stopwords.
- `text_for_embedding`: chuỗi dùng để tạo embedding, ghép từ `clean_title` và `clean_content`.

## Quy trình tiền xử lý

1. Gom dữ liệu từ toàn bộ file JSON.
2. Chuẩn hóa schema về format bài viết chung.
3. Loại bản ghi thiếu `title` hoặc `content`.
4. Loại trùng theo `id`, sau đó loại trùng theo cặp `title` và `content`.
5. Làm sạch text: bỏ HTML, URL, ký tự thừa, chuẩn hóa khoảng trắng.
6. Lowercase, tokenize theo khoảng trắng, remove Vietnamese stopwords cơ bản.
7. Sinh `text_for_embedding` để dùng chung cho TF-IDF, BERT, FAISS và import database.

## Embedding Baseline

- TF-IDF: nhanh, nhẹ, dễ giải thích, phù hợp baseline keyword search.
- BERT/SentenceTransformer: nặng hơn nhưng bắt ngữ nghĩa tốt hơn, phù hợp semantic search.
- Script so sánh: `scripts/compare_embeddings.py`.
