# ECG Learning Portal: Architecture & Workflow Guide

## 1. Why This Project Exists
The ECG Learning Portal is a V1 prototype built to evaluate whether a vision AI model can accurately interpret 12-lead Electrocardiogram (ECG) images to serve as a helpful second opinion for medical students learning cardiac electrophysiology.

## 2. Technology Stack
- **Python (3.11):** Data ingestion, filtering, and plotting.
- **`wfdb` & `pandas`:** Parsing PhysioNet PTB-XL ECG records and clinical metadata.
- **`matplotlib`:** Generating clean 12-lead ECG plots without diagnostic text overlay.
- **`scikit-learn`:** Computing accuracy, confusion matrices, and classification metrics.
- **Plain HTML / CSS / Vanilla JavaScript:** Zero-dependency, ultra-fast frontend quiz interface.

## 3. Complete Workflow
1. **Data Ingestion & Filtering (`backend/scripts/select_records.py`):**
   - Downloads PTB-XL metadata (`ptbxl_database.csv`, `scp_statements.csv`).
   - Filters human-validated single-diagnosis records across 6 classes: Normal, AFIB, CLBBB, CRBBB, IMI, 1AVB.
   - Selects 48 unique patient records (8 per class) and outputs `selected.csv`.
2. **ECG Image Rendering (`backend/scripts/generate_images.py`):**
   - Reads raw signal data via `wfdb`.
   - Plots standard 12-lead grid layouts and saves anonymized PNGs into `frontend/public/images/`.
3. **AI Evaluation (`backend/scripts/ai_query.py` & `evaluate.py`):**
   - Queries or simulates vision AI second opinions (`ai_answers.json`).
   - Evaluates performance with `scikit-learn` (`results.md`).
4. **Interactive Quiz (`backend/scripts/build_quiz.py` & `frontend/public/index.html`):**
   - Selects stratified quiz items into `quiz_data.json`.
   - Renders an interactive student quiz page with instant feedback, ground truth disclosure, and AI reasoning.
