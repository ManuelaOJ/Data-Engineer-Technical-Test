# Data Engineer - Technical Test  

Welcome! This 24‑hour challenge assesses your ability to **orchestrate data pipelines**, **automate ingestion**, and **handle unstructured sources (PDF)**.  
The structure and deliverables mirror our Data Engineer test.

---

<h3>📌 Overview</h3>

<p>
During this 24-hour technical challenge, you will demonstrate your ability to design and implement modern data pipelines using real-world, semi-structured data sources.
</p>

<p>You are expected to:</p>
<ol>
  <li>
    <strong>Ingest</strong> unstructured quarterly PDF reports from a public financial website and store them in a raw <code>bronze</code> layer with metadata and version control.
  </li>
  <li>
    <strong>Extract and normalize</strong> all tabular data from one specific report (<em>Q1 2025</em>), converting it into a structured, analysis-friendly <code>silver</code> dataset.
  </li>
  <li>
    <strong>Design a scalable pipeline architecture</strong> that can orchestrate the end-to-end workflow, support extraction from scanned tables (images), and prepare AI-ready <code>gold</code> data suitable for downstream use by ML models and LLMs.
  </li>
</ol>

<p><strong>Your work will be assessed based on:</strong></p>
<ul>
  <li>Automation, modularity, and reproducibility</li>
  <li>Data modeling, normalization, and metadata tracking</li>
  <li>Scalability and cloud-readiness of your architecture</li>
  <li>Clarity and professionalism in documentation and diagrams</li>
</ul>

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

<h3>✅ Task 3 – Pipeline Design, Orchestration & LLM-Ready Data Strategy</h3>

<h4>📘 Overview</h4>
<p>
This is a <strong>theoretical design challenge</strong>. You are not expected to write code or build a working solution.
Instead, we will assess your ability to:
</p>
<ul>
  <li>Design scalable and modular data architectures</li>
  <li>Select appropriate tools and technologies</li>
  <li>Communicate complex pipelines visually and logically</li>
  <li>Think critically about automation, AI-readiness, and cloud infrastructure</li>
</ul>

<hr>

<h4>🎯 Goal</h4>
<p>
Design a complete and scalable solution to automate the extraction of structured information from quarterly financial reports (PDFs), including documents that contain tables embedded as images. Propose a clear architecture to orchestrate and deploy the entire process in the cloud, preferably using Azure.
</p>

<h4>🧩 Part 1 – Strategy for Scalable Table Extraction</h4>
<p>
Explain how you would design a robust and automated pipeline that:
</p>
<ul>
  <li>Processes multiple quarterly PDF reports from 2021 to 2025.</li>
  <li>Extracts tables from:
    <ul>
      <li><strong>Vector-based PDFs</strong> (standard text-based content)</li>
      <li><strong>Non-vector PDFs</strong> (scanned images or embedded table graphics)</li>
    </ul>
  </li>
</ul>

<p><strong>Your proposal must include:</strong></p>
<ul>
  <li>Preprocessing steps and tools (e.g., OCR, table detection)</li>
  <li>Libraries or frameworks (e.g., <code>pdfplumber</code>, <code>camelot</code>, <code>layoutparser</code>, <code>docTR</code>, <code>tesseract</code>)</li>
  <li>Optional use of LLMs or computer vision models to improve accuracy and structure</li>
</ul>

<h4>⚙️ Part 2 – Orchestration and Automation</h4>
<p>
Design a modular and scalable orchestration strategy to automate the full workflow:
</p>
<ul>
  <li>Automatic detection of new files</li>
  <li>Execution of ingestion, extraction, validation and storage across <strong>Bronze → Silver → Gold</strong> layers</li>
  <li>Metadata tracking, logging, and lineage</li>
</ul>

<p><strong>Be sure to describe:</strong></p>
<ul>
  <li>The orchestration tools you'd use (e.g., <code>Airflow</code>, <code>Azure Data Factory</code>, <code>Prefect</code>)</li>
  <li>How you'd handle scheduling, retries, versioning, and scale</li>
</ul>

<h4>🤖 Part 3 – Gold Layer Design for ML & LLMs</h4>
<p>
Describe how you would structure a <strong>Gold layer</strong> suitable for:
</p>
<ul>
  <li>Machine learning pipelines (e.g., time series, anomaly detection)</li>
  <li>LLM-based applications and Retrieval-Augmented Generation (RAG)</li>
</ul>

<p><strong>Your design should consider:</strong></p>
<ul>
  <li>Normalization and linking of metrics across quarters</li>
  <li>Multilingual support (e.g., English and Spanish)</li>
  <li>Standardized formats (currency, dates, taxonomy)</li>
  <li>Output formats compatible with LLMs (e.g., JSONL, entity-level tables, embedding-friendly formats)</li>
</ul>

<h4>☁️ Part 4 – Cloud Architecture in Azure</h4>
<p>
Outline how the full solution would be deployed in <strong>Microsoft Azure</strong>:
</p>
<ul>
  <li><strong>Storage:</strong> Azure Data Lake, Blob Storage, Delta Lake</li>
  <li><strong>Compute:</strong> Azure ML, Azure Functions, Databricks</li>
  <li><strong>Monitoring:</strong> logging, retries, alerting, dashboards</li>
  <li><strong>Security:</strong> RBAC, Key Vault, service principals</li>
</ul>

<h4>📐 Deliverables</h4>
<ol>
  <li>
    A technical explanation in <code>.md</code>, <code>.ipynb</code> or PDF format covering all four parts.
  </li>
  <li>
    A <strong>mandatory architecture diagram</strong> illustrating your proposed pipeline.
    <ul>
      <li>Use tools like draw.io, Lucidchart, Excalidraw, etc.</li>
      <li>The diagram must show the flow from ingestion to the Gold layer.</li>
      <li>Clearly identify components for orchestration, storage, and any AI/LLM integration points.</li>
    </ul>
  </li>
</ol>

<h4>📌 Evaluation Criteria</h4>
<ul>
  <li>Clarity and modularity of the proposed architecture</li>
  <li>Appropriate use of tools and technologies</li>
  <li>Scalability, maintainability, and automation potential</li>
  <li>Ability to communicate complex processes through visual design</li>
</ul>

---

<h3>🚚 Submission Instructions</h3>

<p>Please organize your submission using the following folder structure:</p>

<pre>
your_name_DataEngTest/
├── task1/               # Ingestion code or notebook
├── task2/               # Table extraction and silver layer output
├── task3/               # Orchestration plan, architecture design, and CI discussion
├── presentation.ppt     # Optional: up to 6-slide summary of your solution
└── README.md            # High-level overview and how to run each task
</pre>

<p><strong>Notes:</strong></p>
<ul>
  <li>Use clear and modular code (e.g., Python scripts or notebooks).</li>
  <li>Document all steps and assumptions directly in the code or notebooks.</li>
  <li>For Task 3, include both your written explanation and the required architecture diagram.</li>
  <li>If needed, use comments or markdown cells to explain decisions or limitations.</li>
</ul>

```

**Repository Requirements:**
- Push to a **public GitHub repository** (or deliver a ZIP)
- Include a comprehensive `README.md` with step-by-step execution instructions

**README.md Must Include:**
- Prerequisites and dependencies installation
- Exact commands to run each task individually
- Complete pipeline execution instructions
- Expected outputs and file locations
- Estimated execution time


---

## 📊 Presentation (.ppt)
Provide up to **6 slides** covering:
1. Approach for each task.  
2. Tools and libraries used.  
3. Pipeline architecture diagram 
4. Validation results   
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

Good luck!
