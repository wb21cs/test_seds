# Paris 2024 — Streamlit Dashboard

Multi-page Streamlit dashboard for visualizing Paris 2024 Olympics data (medals, countries, athletes, and sports).

This 3-day school project was built by:
- BEN TERKI Abdel Ouakil (me)
- BENAYAD Mohammed Amjed ([github link](https://github.com/BNAmjed))

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

---

## Design Choices & Creative Ideas
We struggled to with a few features especially since the dataset is a bit complicated and big, but we still managed to find a way through it.

### Continents:
The country code provided isn't compatible with ISO alpha2 and ISO alpha3, so we had to implement a converter that converts these codes into the suitable format, then allowing us to make a new continent column easily.

### Athlete Images:
Since the dataset lacks any image reference for the athletes, we figured that we can scrape it from the official website of the olympics, and actually we did just that. We still had difficulties figuring out athlete's family names and first names and that made it slightly hard it to fetch the right athlete page, but it wasn't really a problem as the solution covers more that 8000 athletes assumably.

### Torch Relay:
We found out that the dataset contains datapoints represening the route of the olympic torch reaching Paris. We figured that we can represent that on a map and build a page specifically for it.

### Design Patterns & Clean Code:
Although we had little to no time to figure out the architecture of the project, we still were able to try and achieve a bit of what every good developer knows and practices -- design patterns:
- We tried to separate responsibility with the `/utils` directory that in theory should gather every utility function that shouldn't be repeated across pages and scripts, but since we had a very short time to figure out the needs of our project, the code still came out messy anyway.
- We tried to achieve higher speed and smoothness using streamlit's `@caching_data`, and that to avoid big calculations like shaping the dataframes and fetching the images from the olympics website.
- We separated the project from global library and package dependencies using `venv`, and that allow us to create a virtual environment that's independent and self contained.
