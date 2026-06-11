# Data Report - Goodreads Books

## Nguon du lieu
- File goc: `data/raw/books.csv`
- Dataset: Best Books Ever / Goodreads books dataset
- So dong ban dau: 52478
- So dong sau tien xu ly: 52390

## Cau truc du lieu sach
- `source_id`: id sach tu dataset goc
- `title`: ten sach
- `author`: tac gia
- `content`: mo ta sach da xoa HTML, URL, ky tu thua
- `category`: genre dau tien, dung nhu nhan/category chinh
- `genres`: danh sach genre da chuan hoa bang dau cham phay
- `embedding_text`: text da lowercase, tokenize co ban, remove stopwords de tao vector
- `rating`, `num_ratings`, `pages`, `publisher`, `publish_date`, `cover_img`: metadata phuc vu hien thi/loc

## Quy trinh tien xu ly
1. Doc cac cot can thiet tu `books.csv`.
2. Xoa ban ghi thieu title.
3. Xoa trung lap theo `bookId`, sau do theo cap `title` + `author`.
4. Lam sach text: HTML unescape, xoa HTML tag, URL, ky tu dac biet va khoang trang thua.
5. Chuan hoa `genres` tu chuoi list thanh chuoi phan tach bang dau cham phay.
6. Tao `category` tu genre dau tien.
7. Tao `embedding_text` tu title, author, category, genres va description da remove stopwords.
8. Export file sach sach sang CSV UTF-8 de import MongoDB/FAISS.

## Thong ke nhanh
- Token trung binh moi document: 105.52

### Missing values sau tien xu ly
| field | value |
| --- | ---: |
| price | 14341 |
| pages | 2363 |
| title | 0 |
| source_id | 0 |
| category | 0 |
| author | 0 |
| genres | 0 |
| language | 0 |
| rating | 0 |
| content | 0 |
| num_ratings | 0 |
| publisher | 0 |
| cover_img | 0 |
| publish_date | 0 |
| bbe_score | 0 |
| bbe_votes | 0 |
| embedding_text | 0 |
| token_count | 0 |

### Top 10 category
| field | value |
| --- | ---: |
| Fiction | 6129 |
| Fantasy | 5541 |
| Unknown | 4615 |
| Romance | 3333 |
| Young Adult | 3138 |
| Nonfiction | 2562 |
| Historical Fiction | 2226 |
| Mystery | 1939 |
| Science Fiction | 1422 |
| Classics | 1137 |

## File dau ra
- Dataset sach: `data/processed/books_clean.csv`
- San sang import DB bang `scripts/import_data.py`.