# Data Report - Preprocessed Dataset

## Nguon du lieu
- File goc: `data/raw/dataset_kaggle_sample_10000.csv`
- So dong ban dau: 10000
- So dong sau tien xu ly: 9995

## Cau truc du lieu sach
- `source_id`: id tu dataset goc
- `title`: tieu de
- `author`: tac gia
- `content`: noi dung da xoa HTML, URL, ky tu thua
- `category`: category chinh
- `genres`: danh sach genre da chuan hoa bang dau cham phay
- `embedding_text`: text da lowercase, tokenize co ban, remove stopwords de tao vector

## Quy trinh tien xu ly
1. Doc cac cot can thiet tu file input.
2. Xoa ban ghi thieu title.
3. Lam sach text: HTML unescape, xao HTML tag, URL, ky tu dac biet va khoang trang thua.
4. Tu dong nhan dien cot bieu dien noi dung phu hop.
5. Export file sang CSV UTF-8 de import MongoDB/FAISS.

## Thong ke nhanh
- Token trung binh moi document: 503.04

### Missing values sau tien xu ly
| field | value |
| --- | ---: |
| title | 5 |
| author | 5 |
| content | 5 |
| source_id | 0 |
| category | 0 |
| genres | 0 |
| language | 0 |
| rating | 0 |
| num_ratings | 0 |
| pages | 0 |
| publisher | 0 |
| publish_date | 0 |
| cover_img | 0 |
| bbe_score | 0 |
| bbe_votes | 0 |
| price | 0 |
| embedding_text | 0 |
| token_count | 0 |

### Top 10 category
| field | value |
| --- | ---: |
| news_dataset | 9995 |

## File dau ra
- Dataset sach: `data/processed/cleaned.csv`
- San sang import DB bang `scripts/import_data.py`.