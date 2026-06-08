# 🌫️ India Air Quality Index (AQI) Analysis

A comprehensive data analysis and machine learning project to explore, visualize, and predict air quality across Indian cities — featuring an interactive Streamlit dashboard.

---

## 📌 Overview

Air pollution is one of India's most pressing environmental challenges. This project analyzes AQI (Air Quality Index) data across multiple Indian cities, uncovers pollution trends, identifies dominant pollutants, and builds ML models to classify health risk levels — all wrapped in an interactive web dashboard.

---

## 🗂️ Project Structure

```
├── final.ipynb          # Main Jupyter notebook (EDA + ML + Dashboard code)
├── Clean.csv            # Cleaned and processed dataset
├── Data8.csv            # Final feature-engineered dataset
├── app.py               # Streamlit dashboard (extracted from notebook)
└── README.md
```

---

## 📊 Dataset

- **Source:** `aqi_india.csv` — historical AQI readings across Indian cities
- **Key columns:**

| Column | Description |
|---|---|
| `state` | Indian state |
| `city` | City name |
| `datetime` | Timestamp of the reading |
| `pm2.5` | Fine particulate matter (µg/m³) |
| `pm10` | Coarse particulate matter (µg/m³) |
| `co` | Carbon Monoxide (µg/m³) |
| `no2` | Nitrogen Dioxide (µg/m³) |
| `so2` | Sulfur Dioxide (µg/m³) |
| `o3` | Ozone (µg/m³) |
| `dust` | Dust concentration (µg/m³) |
| `us_aqi` | US AQI value |
| `AQI_Class` | AQI category (Good → Severe) |
| `risk_level` | Derived risk label (Low / Medium / High) |

---

## ⚙️ Workflow

### 1. Data Cleaning
- Removed duplicate rows
- Renamed columns for readability (`pm2_5_ugm3` → `pm2.5`, etc.)
- Dropped null values and irrelevant columns
- Parsed `datetime` with mixed format handling

### 2. Feature Engineering
- **AQI Category** — classified AQI into 6 levels: Good, Satisfactory, Moderate, Poor, Very Poor, Severe
- **Risk Level** — mapped AQI categories to Low / Medium / High risk
- **Pollution Intensity Score** — normalized AQI (0–1 scale)
- Extracted `year`, `month`, and `month_name` from datetime

### 3. Exploratory Data Analysis (EDA)
- AQI trend over time (static + interactive with Plotly)
- Top 10 most polluted cities
- PM2.5 vs AQI scatter plot with regression line
- PM10 vs AQI scatter plot
- Monthly average AQI bar chart
- AQI category distribution

### 4. Machine Learning
Predicts **health risk level** (`Low` / `Medium` / `High`) from pollutant features.

| Model | Features Used |
|---|---|
| Decision Tree | pm2.5, pm10, no2, so2, co, o3, year, month |
| Random Forest | pm2.5, pm10, no2, so2, co, o3, year, month, city, season |

- Train/test split: 80/20 with stratification
- Preprocessing: Median imputation for numerical; One-Hot Encoding for categorical
- Class imbalance handled via `class_weight="balanced"`

### 5. Streamlit Dashboard
Interactive city-level AQI dashboard featuring:
- City selector (sidebar)
- KPI metrics: Average AQI, Max AQI, Dominant AQI Class, Risk Category
- Dominant pollutant table
- Health advisory message
- AQI trend line chart
- AQI category distribution bar chart
- Filtered raw data preview

---

## 🖥️ Running the Dashboard

### Prerequisites

```bash
pip install pandas numpy matplotlib seaborn plotly scikit-learn streamlit
```

### Launch the App

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

> **Note:** Make sure `ready.csv` (the cleaned dataset) is in the same directory as `app.py`.

---

## 📈 Key Insights

- **PM2.5 is the dominant driver** of high AQI values across most Indian cities.
- **Winter months** (November–January) consistently show higher pollution levels due to meteorological conditions and increased burning activity.
- Several cities in northern India regularly fall in the **Poor to Severe** AQI range.
- The Random Forest model outperforms the Decision Tree in classifying health risk levels.

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3 |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn, Plotly |
| Machine Learning | Scikit-learn (Decision Tree, Random Forest) |
| Dashboard | Streamlit |
| Notebook | Jupyter Notebook |

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
