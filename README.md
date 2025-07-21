# Data Engineer Technical Test  
*SV‑Exploration · OreOptix AI*

Welcome! This 24‑hour challenge assesses your ability to **orchestrate data pipelines**, **automate ingestion**, and **handle unstructured sources (PDF)**.  
The structure and deliverables mirror our Data Engineer test.

---

## 📌 Overview  
During the exercise you will:
1. **Ingest** unstructured PDF reports from a public website.  
2. **Transform** the information into **Bronze → Silver** layers with proper logging.  
3. **Orchestrate & validate** the pipeline using CI/CD best practices.

---

<h3>✅ Task 1 – Automated Report Ingestion</h3>

<h4>Goal</h4>
<p>
  Build a repeatable and idempotent process that automatically downloads company reports and stores them in the Bronze layer.
</p>

<h4>Instructions</h4>
<ol>
  <li>
    Visit the <strong>Mineros S.A. Financial Reports</strong> page:<br>
    <a href="https://www.mineros.com.co/investors/financial-reports" target="_blank">
      https://www.mineros.com.co/investors/financial-reports
    </a>
  </li>

  <li>
    <strong>Download exclusively the quarterly "Consolidated Financial Statements" PDFs (Q1, Q2, Q3, Q4) published between 2021 and 2024.</strong><br>
    Do <strong>not</strong> include other types of reports.
  </li>
  <img width="1167" height="673" alt="image" src="https://github.com/user-attachments/assets/98296fbc-5c3c-4470-8f8a-283420152fb9" />


  <li>
    Save each file <strong>unchanged</strong> in the following folder structure:<br>
    <code>bronze/&lt;year&gt;_Q&lt;quarter&gt;/&lt;filename&gt;.pdf</code><br>
    Example: <code>bronze/2023_Q4/Consolidated_Financial_Statements_Q4_2023.pdf</code>
  </li>

  <li>
    For each downloaded file, register the following metadata in a single Parquet file named <code>metadata_bronze.parquet</code>:
    <ul>
      <li><code>filename</code></li>
      <li><code>filesize</code> (in bytes)</li>
      <li><code>sha256</code> (hash of the file)</li>
      <li><code>download_timestamp</code> (UTC)</li>
    </ul>
  </li>

  <li>
    The process must be <strong>idempotent</strong>:<br>
    If a file with the same SHA256 hash already exists in the metadata, it should be skipped.
  </li>

  <li>
    You are free to use any tools or scripting languages you prefer to automate the solution (e.g., Python, Bash, Puppeteer, RPA, etc.).
  </li>
</ol>


---

### ✅ Task 2 – Table Extraction & Silver Layer  
**Goal**  
Extract structured financial tables and load them into a Silver dataset.

**Instructions**
1. Inside the **Consolidated Financial Statements** PDFs, locate the *Statement of Profit or Loss*.  
2. **Select any 4 key financial metrics** from the statements (e.g., Revenue, Gross Profit, Operating Expenses, Net Income, etc.).  
3. Extract these metrics for **all available quarters** and normalize the data.  
4. Write consolidated data to `silver/income_statements.parquet` with columns:  
   `year`, `quarter`, `metric`, `value_local`, `currency`.  
5. Implement a **data‑quality rule**: compute the **% of selected metrics present per quarter** and log results to `dq_log.jsonl`.

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
# [Your Name] - Mineros S.A. Data Engineering Test

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
