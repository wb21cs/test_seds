# Paris 2024 — Streamlit Dashboard

Multi-page Streamlit dashboard for visualizing Paris 2024 Olympics data (medals, countries, athletes, and sports).

---

## Quick Start

These steps assume you already have **Python 3.10+** and **git** installed.

### 1. Clone the repository

```bash
git clone https://github.com/wb21cs/test_seds
cd test_seds
```

---

### 2. Create and activate a virtual environment

> This keeps dependencies isolated from your system Python.

**Linux / macOS**

```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Run the app from the entry file `1_Overview.py`

```bash
streamlit run 1_Overview.py
```

The app will open in your browser (usually at `http://localhost:8501`).
