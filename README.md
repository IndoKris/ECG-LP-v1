# ECG Learning Portal (V1 Prototype)

A lightweight educational prototype testing whether a vision AI model can interpret 12-lead ECGs to assist medical students, complete with an interactive quiz interface.

## Project Structure

```text
ECG Learning Portal/
├── PRD.md
├── frontend/
│   └── public/
│       ├── index.html          # Interactive student quiz portal
│       ├── quiz_data.json      # Quiz dataset & AI second opinions
│       └── images/             # 48 generated 12-lead ECG PNGs
└── backend/
    ├── ptbxl_data/             # PTB-XL metadata (CSV)
    ├── data/                   # Processed records, answers, results
    └── scripts/                # Pipeline Python scripts
```

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/indokris/ECG-LP-v1.git
   cd "ECG-LP-v1/frontend/public"
   ```

2. **Run a local web server:**
   ```bash
   python3 -m http.server 8000
   ```

3. **Open in browser:**
   `http://localhost:8000/index.html`

---
*For educational purposes only. Not for diagnosing or treating patients.*
