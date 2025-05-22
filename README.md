# 📈 Futu US Stock Options Dashboard

A Streamlit app to **fetch and visualize US stock options data** (TSLA, AAPL, NVDA) using the **Futu OpenD API** or a sample `.csv`.

## 🔧 Features

- 📊 Filter options by Open Interest > 0 and Expiry > today
- 🧠 Visualizations by Strike Price
- 📥 Download filtered data as CSV
- ⚡ Streamlit caching for better performance

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/futu-options-dashboard.git
cd futu-options-dashboard
```

### 2. Install Dependencies

It's recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Start Streamlit App

```bash
streamlit run app.py
```

---

## 📦 Folder Structure

```
futu-options-dashboard/
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
└── US_TSLA_filtered_options.csv
```

---

## 🖥️ Notes for Live Futu API Use

- Ensure `FutuOpenD` is running on your local machine (port 11111).
- You must be logged in with a valid Futu account.
- For more details, visit [Futu OpenAPI Docs](https://openapi.futunn.com/)

---

## 📄 License

MIT License
