# 📊 Streamlit Financial Transactions Dashboard

This project is an interactive dashboard built with **Streamlit** to explore and analyze financial transaction data in a business intelligence style. The application is structured following a **star schema model**, integrating fact and dimension tables, and supports both time-based and country-based exploration.

#Key Features

- **Time Analysis Page**:
  - Interactive date range filtering
  - Line chart showing total transactions over time
  - Top 3 traded symbols
  - Top 5 sectors and industries by transaction count

- **Country Analysis Page**:
  - Country selector based on the company’s origin
  - Weekly line chart of BUY and SELL trends
  - Summary metrics of transactions per country
  - Top 5 industries by BUY and SELL transactions

#Project Structure

```
Streamlit_Dashboard_ValerioBotto/
│
├── data/                 # CSV files: fact table and dimension tables
├── pages/                # Streamlit pages: TimeAnalysis and CountryAnalysis
├── utils/                # Reusable plotting and data loader functions
├── Frontpage.py          # Landing page of the dashboard
├── requirements.txt      # Python dependencies
├── README.md             # This file
└── .gitignore
```

## ▶️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/ValerioBotto/Streamlit-Financial-Transactions-Dashboard.git
cd Streamlit-Financial-Transactions-Dashboard
```

### 2. Create a Virtual Environment

It is recommended to use a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate      # On Windows: .venv\Scripts\activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Launch the Dashboard

```bash
streamlit run Frontpage.py
```

Then, open the displayed local URL (e.g. `http://localhost:8501`) in your browser.

## 💡 Notes

- This dashboard uses **Plotly** for interactive charts.
- All datasets used in the dashboard are included in the `/data` folder.
- Streamlit navigation is handled using multipage support (`pages/` folder).

## 📌 Requirements

See `requirements.txt` for specific library versions. Main dependencies:

- `streamlit==1.35.0`
- `pandas==2.3.0`
- `plotly==6.1.2`

## 📬 Contact

Developed by **Valerio Botto**  
Feel free to connect on [LinkedIn](https://www.linkedin.com/) or check out the repository for future updates!

---

© 2025 Università di Catania — For educational purposes.
