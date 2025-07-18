# Data Engineer Technical Test  
*sun valley investments*

Welcome! This 24‑hour challenge assesses your ability to **orchestrate data pipelines**, **automate ingestion**, and **handle unstructured sources (PDF)**.  
The structure and deliverables mirror our Data Engineer test.

---

## 📌 Overview  
During the exercise you will:
1. **Ingest** unstructured PDF reports from a public website.  
2. **Transform** the information into **Bronze → Silver** layers with proper logging.  
3. **Orchestrate & validate** the pipeline using CI/CD best practices.

---

## 📂 Tasks  

### ✅ Task 1 – Automated Report Ingestion  
**Goal**  
Build a repeatable process that downloads company reports and stores them in a Bronze layer.

**Instructions**
1. Visit **Mineros S.A. Financial Reports**  
   <https://www.mineros.com.co/investors/financial-reports>  
2. Download **all PDFs** published between **2021 and 2024**.  
3. For each file:  
   - Save it unchanged in `bronze/<year>_Q<quarter>/` (e.g., `bronze/2023_Q4/`).  
   - Record `filename`, `filesize`, `sha256`, and `download_timestamp` in `metadata_bronze.parquet`.  
4. The ingestion must be **idempotent**: if a file with the same hash already exists, skip it.

---

### ✅ Task 2 – Table Extraction & Silver Layer  
**Goal**  
Extract structured financial tables and load them into a Silver dataset.

**Instructions**
1. Inside the **Consolidated Financial Statements** PDFs, locate the *Statement of Profit or Loss*.  
2. Extract the table and normalise headers (`Revenue`, `Cost of Sales`, `EBITDA`, etc.).  
3. Write each quarter to `silver/income_statements.parquet` with columns:  
   `year`, `quarter`, `metric`, `value_local`, `currency`.  
4. Implement a **data‑quality rule**: compute the **% of expected metrics present** and log it to `dq_log.jsonl`.

---

### ✅ Task 3 – Orchestration & CI/CD  
**Goal**  
Build a minimal scheduler and configure CI with lint + tests.

**Instructions**
1. Use **Prefect**, **Airflow**, or a custom Python CLI (`pipeline.py run all`).  
2. Pipeline stages: `ingest → extract → quality_check`.  
3. Provide a **GitHub Actions** workflow that:  
   - Installs dependencies.  
   - Runs `black --check` + `ruff`.  
   - Executes unit tests in `tests/`.  
4. Include a sample `pytest` that mocks one PDF and asserts correct Parquet output.

---

## 🚚 Submission Instructions  

Organise your repository as follows:

```
your_name_DataEngTest/
├── task1/               # Ingestion code / notebook
├── task2/               # Extraction + silver layer
├── task3/               # Orchestration + CI config
├── presentation.ppt     # Max 6-slide presentation
└── README.md           # How to run everything
```

**Repository Requirements:**
- Push to a **public GitHub repository** (or deliver a ZIP)
- Ensure the GitHub Actions workflow passes
- Include a comprehensive `README.md` with step-by-step execution instructions

**README.md Must Include:**
- Prerequisites and dependencies installation
- Exact commands to run each task individually
- Complete pipeline execution instructions
- Expected outputs and file locations
- Estimated execution time

**Example README structure:**
```markdown
# [Your Name] - sun valley investments Data Engineering Test

## Prerequisites
- Python 3.8+
- Required packages: pandas, PyPDF2, requests, prefect

## Installation
```bash
pip install -r requirements.txt
```

## How to Run Everything

### Task 1: Download Reports
```bash
cd task1
python ingest_reports.py
```

### Task 2: Extract Tables  
```bash
cd task2
python extract_tables.py
```

### Task 3: Run Complete Pipeline
```bash
cd task3
python pipeline.py run all
```

## Expected Outputs
- `bronze/` folders with PDFs organized by year/quarter
- `silver/income_statements.parquet`
- `metadata_bronze.parquet`
- `dq_log.jsonl`

**Execution time**: ~15-20 minutes
```

---

## 📊 Presentation (.ppt)
Provide up to **6 slides** covering:
1. Approach for each task.  
2. Tools and libraries used.  
3. Pipeline architecture diagram (Bronze → Silver).  
4. Validation results & logs.  
5. Improvement ideas.

---

## ✅ Evaluation Criteria  
| Aspect                                  | Weight |
|-----------------------------------------|--------|
| Correctness of ingestion & extraction   | 35%    |
| Pipeline orchestration & idempotence    | 25%    |
| Code quality (structure, style, tests)  | 20%    |
| Data‑quality logging & validation       | 10%    |
| Clarity of the presentation             | 10%    |

---

## ⏱️ Time Limit & Delivery
- **24 hours** from receiving this brief.  
- Send the repository link (or ZIP) and the last commit SHA to  
  **reclutamiento@sunvalleyinvestment.com**.  
- Technical questions will be answered only within the first **4 hours**.

---

Good luck!

