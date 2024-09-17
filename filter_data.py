import polars as pl
import os

df = pl.read_ndjson("archive\arxiv-metadata-oai-snapshot.json")

cs_data = df.filter(pl.col("categories").str.contains(r"\b(?:cs\.(?:CV|LG|CL|AI|NE|RO))\b", strict=True))

drop = ['versions', 'authors_parsed', 'report-no', 'license', 'submitter','categories',
       'id', 'authors', 'comments', 'journal-ref', 'doi','update_date']
train = cs_data.drop(drop)
train

train.write_ndjson("data/filtered.json")

df = pl.read_ndjson("data/filtered.json")

csv_file_path = 'filtered_data.csv' 
df.write_csv(csv_file_path)