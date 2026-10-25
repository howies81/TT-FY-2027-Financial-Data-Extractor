# Unstructured PDF Data Extraction & Transformation Pipeline

A programmatic data engineering pipeline built in Python using `pymupdf`, `pandas`, `numpy`, and `openpyxl` to extract, clean, and structure complex financial tables from public economic reports into production-ready Excel datasets.

## The Technical Challenge
Public macroeconomic documents are frequently distributed as complex layout PDFs. Standard out-of-the-box parsing utilities fail to process them accurately due to structural anomalies:
* **Wrapped Row Labels:** Text strings spilling over multiple vertical lines, causing row index fragmentation.
* **Shifting Column Boundaries:** Micro-variations in character coordinates across shifting financial years.
* **Tabular Metadata Noise:** Footnote markers, revision symbols (e.g., 'r', 'p'), and empty cells disrupting numerical data fields.

## Toolstack & Core Architecture
This solution bypasses manual data entry by executing a coordinate-based algorithmic parsing workflow:
* **`pymupdf` (fitz):** Deployed to evaluate raw structural text locations, programmatically matching text fragments dynamically based on their right-hand alignment boundaries.
* **`pandas` & `numpy`:** Utilized to handle data type cleaning, merge broken row labels by spatial position, filter out empty rows, and structure data fields into clean, logical DataFrames.
* **`openpyxl`:** Employed to compile, format, and serialize the finalized data arrays straight into multi-sheet Excel workbooks.

## Extracted Data Assets
The resulting structural matrices are organized within the repository directory, mapping granular macroeconomic trends:
1. **Central Government Financing:** Structured sheets capturing real Government financing metrics, including borrowing, capital repayments (Domestic and External) and HSF transfers.
2. **T&T Natural Gas Production and Utilisation Data:** Natural Gas and natural gas derivative production data.


## Local Environment Execution
To run the extraction pipeline locally, install the core execution stack and run the primary script:
```bash
pip install pymupdf pandas numpy openpyxl
python tt_fy2027_financing_data.py
python tt_fy2027_natgasprod2026.py
```