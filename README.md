# 🎵 Spotify Data Engineering on AWS — Learn by Building

## 📌 Objective
This project is designed as a **hands-on guide** to understanding how to **integrate multiple AWS services** to build a simple, end-to-end **data engineering pipeline**.  
It's suitable for beginners and intermediate learners who want to learn:

- How to **store and organize raw data** in Amazon S3
- How to **process and transform data** with AWS Glue (PySpark)
- How to **validate data quality** before storing results
- How to **query transformed data** with Amazon Athena
- How to **visualize results** using Amazon QuickSight

By the end you will not only be able to reproduce the pipeline, you'll understand why each component is used and how they connect.

---

## 🏗️ Architecture
Add your architecture diagram to `images/architecture.png`. A placeholder image has been included.

---

## 🚀 Workflow
1. **Ingest Data** → Upload Spotify dataset (albums, artists, tracks) to the S3 *staging* prefix.
2. **ETL Processing** → AWS Glue job joins and cleans data, applies **data quality rules**, writes to *data-warehouse* in Parquet (Snappy).
3. **Catalog Data** → AWS Glue Crawler registers Parquet data in the AWS Glue Data Catalog.
4. **Query with Athena** → Run SQL queries on transformed data directly from S3.
5. **Visualize in QuickSight** → Build dashboards showing top artists, album counts, and track distributions.

---

## 🛠️ Tools & Technologies
- **Amazon S3** — Store raw and processed data
- **AWS Glue** — Serverless ETL (PySpark)
- **AWS Glue Crawler** — Schema discovery & cataloging
- **Amazon Athena** — Ad-hoc SQL on data stored in S3
- **Amazon QuickSight** — BI dashboards and visuals

---

## 📂 Repo Structure
```
spotify-data-engineering-aws/
│
├── README.md
├── LICENSE
├── .gitignore
├── code/
│   └── glue_etl_job.py
├── docs/
│   ├── project_transcript.md
│   └── dataset_description.md
├── sql/
│   └── athena_queries.sql
├── quicksight/
│   └── README.md
├── scripts/
│   └── deploy_iam_role.sh
├── images/
│   └── architecture.png
└── examples/
    └── sample_queries.md
```

---

## 🔧 Quick start (local + AWS)
1. **Clone** the repo (or download the ZIP included with this project).
2. **Upload** your cleaned CSVs to S3 staging:
   - `s3://<your-bucket>/staging/albums.csv`
   - `s3://<your-bucket>/staging/artists.csv`
   - `s3://<your-bucket>/staging/track.csv`
3. **Create** an IAM role for Glue (use `scripts/deploy_iam_role.sh` or create via console). Attach `AmazonS3FullAccess` and `AWSGlueServiceRole` (or least-privilege policies).
4. **Create** a Glue job, upload `code/glue_etl_job.py`, set:
   - Glue version: 3.0 or 4.0 (python 3.x)
   - Worker type: G.1X / G.2X
   - Number of workers: 2–5 (for small datasets)
   - IAM Role: the role created earlier
   - Job arguments: `--JOB_NAME`, (Glue injects this automatically)
5. **Run** the job. Output will be at: `s3://<your-bucket>/data_warehouse/` in Parquet (snappy).
6. **Create** a Glue Crawler on that prefix to register a table in a Glue DB (e.g., `spotify_db`).
7. **Run** Athena queries (set query results S3 location).
8. **Connect** QuickSight to Athena and build dashboards.

---

## 📚 Learning outcomes
- How to design a simple data lake layout in S3
- How to author a Glue ETL job (PySpark) and apply built-in data quality checks
- How Glue Crawlers and the Glue Data Catalog enable Athena queries
- How to build quick visualizations in QuickSight for stakeholders

---

## Files to customize
- `images/architecture.png` — replace placeholder with your architecture screenshot
- `code/glue_etl_job.py` — the production Glue job (already included)
- `docs/project_transcript.md` — cleaned transcript (already included)
- `sql/athena_queries.sql` — example analytics queries

---

## License
MIT — see `LICENSE`.

