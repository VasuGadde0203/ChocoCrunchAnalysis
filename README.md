# 🍫 Choco Crunch Analysis
### SQL + Streamlit End-to-End Nutrition Analytics Project

<br>

## 📖 Project Overview

This project performs a complete **end-to-end data analytics workflow** on chocolate product nutritional data sourced from the Open Food Facts API.

It covers:

- 🌐 API-based data extraction from Open Food Facts
- 🧹 Data cleaning & feature engineering using Pandas
- 🗄️ SQL database design with a normalized 3-table schema
- 💾 Data insertion into MySQL
- 🔎 Advanced SQL analytics (27 analytical queries)
- 📊 Interactive analytics dashboard built using Streamlit + Plotly
- ❤️ Health-risk pattern analysis across brands, NOVA groups, and categories

The goal is to demonstrate how raw product data can be transformed into **meaningful consumer health insights** using data engineering and analytics techniques.

---

## 🏗️ Project Architecture

```
Data Collection (Open Food Facts API)
        ↓
Data Cleaning & Feature Engineering (Pandas)
        ↓
MySQL Database (3 Normalized Tables)
        ↓
SQL Analytics (27 Queries)
        ↓
Streamlit Interactive Dashboard
```

---

## 🗃️ Database Design

The project uses a **normalized 3-table relational schema** in MySQL:

### 1️⃣ product_info
| Column | Type | Description |
|--------|------|-------------|
| product_code | VARCHAR (PK) | Unique product barcode |
| product_name | TEXT | Name of the product |
| brand | VARCHAR | Brand name |

### 2️⃣ nutrient_info
| Column | Type | Description |
|--------|------|-------------|
| product_code | VARCHAR (FK) | References product_info |
| energy_kcal_value | FLOAT | Energy in kcal per 100g |
| energy_kj_value | FLOAT | Energy in kJ per 100g |
| carbohydrates_value | FLOAT | Carbohydrates per 100g |
| sugars_value | FLOAT | Sugars per 100g |
| fat_value | FLOAT | Total fat per 100g |
| saturated_fat_value | FLOAT | Saturated fat per 100g |
| proteins_value | FLOAT | Proteins per 100g |
| fiber_value | FLOAT | Dietary fiber per 100g |
| salt_value | FLOAT | Salt per 100g |
| sodium_value | FLOAT | Sodium per 100g |
| fruits_veg_nuts_100g | FLOAT | Fruits/vegetables/nuts estimate |
| nutrition_score_fr | FLOAT | Nutri-Score (FR) |
| nova_group | INT | NOVA processing classification (1–4) |

### 3️⃣ derived_metrics
| Column | Type | Description |
|--------|------|-------------|
| product_code | VARCHAR (FK) | References product_info |
| sugar_to_carb_ratio | FLOAT | Sugars ÷ Carbohydrates |
| calorie_category | VARCHAR | Low / Medium / High Calorie |
| sugar_category | VARCHAR | High Sugar / Low Sugar |
| is_ultra_processed | TINYINT | 1 if NOVA group = 4, else 0 |

This structure enables **efficient joins**, clean separation of concerns, and scalable analytics.

---

## 📊 SQL Analytics — 27 Queries

### 📑 product_info Queries
| # | Query |
|---|-------|
| 1 | Count products per brand |
| 2 | Count unique products per brand |
| 3 | Top 5 brands by product count |
| 4 | Products with missing product name |
| 5 | Number of unique brands |
| 6 | Products with code starting with '3' |

### 📑 nutrient_info Queries
| # | Query |
|---|-------|
| 7 | Top 10 products with highest energy-kcal_value |
| 8 | Average sugars_value per nova-group |
| 9 | Count products with fat_value > 20g |
| 10 | Average carbohydrates_value per product |
| 11 | Products with sodium_value > 1g |
| 12 | Count products with non-zero fruits-vegetables-nuts content |
| 13 | Products with energy-kcal_value > 500 |

### 📑 derived_metrics Queries
| # | Query |
|---|-------|
| 14 | Count products per calorie_category |
| 15 | Count of High Sugar products |
| 16 | Average sugar_to_carb_ratio for High Calorie products |
| 17 | Products that are both High Calorie and High Sugar |
| 18 | Number of products marked as ultra-processed |
| 19 | Products with sugar_to_carb_ratio > 0.7 |
| 20 | Average sugar_to_carb_ratio per calorie_category |

### 📑 Join Queries
| # | Query |
|---|-------|
| 21 | Top 5 brands with most High Calorie products |
| 22 | Average energy-kcal_value for each calorie_category |
| 23 | Count of ultra-processed products per brand |
| 24 | Products with High Sugar and High Calorie along with brand |
| 25 | Average sugar content per brand for ultra-processed products |
| 26 | Number of products with fruits/vegetables/nuts in each calorie_category |
| 27 | Top 5 products by sugar_to_carb_ratio with calorie and sugar category |

---

## 📈 Interactive Dashboard (Streamlit)

The Streamlit app replaces Power BI and serves as a fully interactive analytics interface.

### 🏠 Home Page
- Live MySQL connection via sidebar credentials
- 5 KPI cards: Total Products · Avg kcal · Avg Sugars · Ultra-Processed Count · High Calorie Count
- Full data preview (joined across all 3 tables)

### 💾 SQL Queries Page
- All 27 queries displayed with syntax-highlighted SQL code
- Live query results rendered as interactive tables
- Key queries auto-render charts below the result table

### 📊 Dashboard Page (15+ Visualizations)

| # | Chart Type | Description |
|---|------------|-------------|
| ① | Bar chart | Number of products in each calorie_category |
| ② | Pie chart | Distribution of products by NOVA group |
| ③ | Horizontal bar | Top 10 brands by average energy-kcal |
| ④ | Scatter plot | Calories vs Sugar content |
| ⑤ | Box plot | Sugar-to-carb ratio distribution by calorie category |
| ⑥ | Treemap | Product count by brand and calorie_category |
| ⑦ | Heatmap | Correlation between calories, sugars, fat, carbs, proteins |
| ⑧ | Horizontal bar | Number of High Sugar products per brand (Top 10) |
| ⑨ | Stacked bar | Ultra-processed vs Not ultra-processed per brand |
| ⑩ | Violin plot | Energy distribution by NOVA group |
| ⑪ | Line chart | Average sugars per NOVA group |
| ⑫ | Donut chart | Sugar category split (High vs Low) |
| ⑬ | Bar chart | Average fat per calorie category |
| ⑭ | Radar chart | Nutritional profile comparison across calorie categories |
| ⑮ | Bar chart | Top 5 products by sugar-to-carb ratio |

**Interactive filters:** Brand · Calorie Category · NOVA Group

### 💡 Insights Page
- Data-driven key findings with live statistics
- Highest health-risk brand profiles table
- NOVA group nutritional comparison (multi-panel chart)
- Consumer, manufacturer, and regulator recommendations

---

## 🧠 Key Insights

- **Ultra-processed (NOVA 4)** chocolates dominate the market and tend to have higher sugar and calorie values compared to lower NOVA groups.
- **Certain brands** consistently appear in the High Calorie + High Sugar segment, representing the highest health-risk profiles.
- **High sugar products strongly correlate** with high energy density — the two risks rarely appear independently.
- **NOVA Group 4 products** show measurably higher average sugars and fat than Groups 1–3.
- Consumers choosing chocolates with **NOVA group 1–2** are exposed to significantly fewer additives and ultra-processing.
- The **sugar-to-carb ratio** is a powerful derived metric — products with ratio > 0.7 are heavily sugar-dominant.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Pandas | Data cleaning & feature engineering |
| MySQL | Relational database |
| mysql-connector-python | Python–MySQL bridge |
| Streamlit | Interactive web dashboard |
| Plotly | Interactive visualizations |
| Open Food Facts API | Data source |

---

## 📂 Project Structure

```
ChocoCrunchAnalysis/
│
├── app.py              # Main Streamlit application
├── db.py               # MySQL connection helper
└── queries.py          # SQL query definitions
├── Data Collection.py      # API data extraction script
├── data_processing.py      # Cleaning & feature engineering
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## 🚀 How to Run Locally

### 1️⃣ Clone the repository
```bash
git clone https://github.com/VasuGadde0203/ChocoCrunchAnalysis.git
cd ChocoCrunchAnalysis
```

### 2️⃣ Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Set up MySQL database
```sql
CREATE DATABASE choco_crunch;
```
Then run your data insertion scripts (`Data Collection.py` → `data_processing.py`) to populate the 3 tables.

### 5️⃣ Launch the Streamlit app
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`, enter your MySQL credentials in the sidebar, and click **Connect to MySQL**.

---

## 📦 requirements.txt

```
streamlit>=1.32.0
pandas>=2.0.0
mysql-connector-python>=8.3.0
plotly>=5.18.0
```

---

## 📌 Learning Outcomes

This project demonstrates proficiency in:

- ✅ Relational database schema design (normalization, FK relationships)
- ✅ Writing and optimizing analytical SQL queries
- ✅ Python-based data cleaning and feature engineering
- ✅ Building production-grade interactive dashboards
- ✅ Full-stack data project delivery (API → DB → Dashboard)
- ✅ Translating raw data into actionable consumer health insights

---

## 📬 Author

**Vasu Gadde**  
Data Analytics & Machine Learning Enthusiast

---
