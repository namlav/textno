# textno

Nhom project mon Khai pha du lieu, su dung Python va NoSQL cho quan ly va tim kiem van ban.

## Dataset

- `data/raw/dataset.csv`: original small dataset kept for compatibility with the current project flow.
- `data/raw/dataset_kaggle_sample_10000.csv`: balanced 10,000-row sample converted from the Kaggle Vietnamese Online News Dataset.

Kaggle source:
https://www.kaggle.com/datasets/haitranquangofficial/vietnamese-online-news-dataset

The Kaggle dataset contains 150K+ Vietnamese online news articles from multiple sources. The project CSV schema is:

```text
id,title,updatetime,wordcount,publication,tags,content,author
```

To rebuild the Kaggle sample:

```powershell
python scripts\prepare_kaggle_news_dataset.py
```

To also generate the full converted dataset locally:

```powershell
python scripts\prepare_kaggle_news_dataset.py --full-output data\raw\dataset_kaggle_full.csv
```

Full converted CSV files are intentionally ignored by Git because they are too large for normal GitHub pushes.
