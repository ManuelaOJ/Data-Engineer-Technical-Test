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
    <strong>Download exclusively the quarterly "Consolidated Financial Statements" PDFs (Q1, Q2, Q3, Q4) published between 2021 and 2025.</strong><br>
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

<h3>✅ Task 2 – Table Extraction & Silver Layer</h3>

<h4>🎯 Goal</h4>
<p>
  Extract <strong>all structured tables</strong> from the PDF report
  <strong>“Consolidated Financial Statements – Q1 2025”</strong> and convert them into a clean, flexible dataset
  suitable for analysis (e.g., in Excel, pandas, or Power BI).
</p>

<h4>📝 Instructions</h4>
<ol>
  <li>
    Use <strong>only</strong> the following PDF file, already downloaded in Task 1:<br>
    <code>bronze/2025_Q1/Consolidated_Financial_Statements_Q1_2025.pdf</code>
  </li>

  <li>
    From this single report, <strong>extract all tables</strong> that are presented in a structured format.<br>
    Do <strong>not</strong> filter or limit the content — include all identifiable tabular data found in the document.
  </li>

  <li>
    Convert the extracted tables into a <strong>normalized (long) format</strong>, where each row represents a single data point.<br>
    Save the entire output in a single Parquet file:<br>
    <code>silver/q1_2025_tables.parquet</code>
  </li>

  <li>
    Each row in the resulting dataset should include the following fields when applicable:
    <ul>
      <li><code>table_name</code> – name or title of the table (if available)</li>
      <li><code>row_label</code> – description of the row (e.g., “Revenue”, “Total Assets”)</li>
      <li><code>column_header</code> – the header or period (e.g., “Q1 2025”, “Q1 2024”)</li>
      <li><code>value</code> – extracted numeric value</li>
      <li><code>currency</code> – default to USD unless stated otherwise</li>
      <li><code>page_number</code> – page number in the PDF where the table appears</li>
    </ul>
  </li>

  <li>
    You may use any tool or library you prefer to perform the extraction, such as:
    <ul>
      <li><code>pdfplumber</code></li>
      <li><code>camelot</code></li>
      <li><code>tabula</code></li>
      <li><code>PyMuPDF</code></li>
    </ul>
  </li>

  <li>
    Optionally, you may use <strong>LLMs or AI-based tools</strong> to:
    <ul>
      <li>Assist in identifying table regions</li>
      <li>Normalize ambiguous row/column labels</li>
      <li>Handle messy or merged table cells</li>
    </ul>
  </li>
</ol>

<h4>📌 Notes</h4>
<ul>
  <li>
    This task simulates a typical Silver-layer transformation:
    converting semi-structured PDF content into structured, liquid data.
  </li>
  <li>
    You do not need to clean or interpret the content — just extract and organize it into a format
    that is easy to manipulate in spreadsheets or pipelines.
  </li>
  <li>
    <strong>Only the Q1 2025 report should be used.</strong> Do not process any other quarterly files.
  </li>
</ul>

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
