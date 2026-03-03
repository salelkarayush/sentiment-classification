# 🛒 E-Commerce Sentiment Classification Pipeline

## 📌 Overview

This project is an **end-to-end machine learning pipeline** that:

- Scrapes product reviews from Flipkart using Selenium
- Cleans and preprocesses noisy real-world text data
- Trains a lightweight sentiment classification model
- Serves predictions through a FastAPI API

The goal of this project is to demonstrate a complete workflow combining:

- Web Scraping
- Data Processing
- Machine Learning
- Backend API Deployment

---

##  Project Structure

ecommerce-sentiment/

│  
├── scraper/  
│   └── scraper.py        # Selenium-based review scraper  

├── data/  
│   └── processing.py     # Data cleaning & preprocessing  

├── models/  
│   └── train.py          # Model training pipeline  

├── main.py               # FastAPI application serving predictions  
├── requirements.txt      # Python dependencies  
├── pyproject.toml        # uv dependency configuration  
└── README.md  

---

## ⚙️ Features

- Scrapes Flipkart reviews from dynamic React pages
- Handles infinite scrolling using Selenium
- Cleans and preprocesses noisy review text
- Trains a lightweight sentiment classification model
- Exposes predictions via FastAPI REST API
- Reproducible development setup using **uv**

---

## 🧰 Tech Stack

- Python
- Selenium
- Pandas & NumPy
- Scikit-learn
- FastAPI
- Uvicorn
- uv (modern Python package manager)

---

# 🚀 Setup Instructions

You can run this project using either:

1. **uv (Recommended — faster & reproducible)**
2. **Traditional pip + requirements.txt**

---

# ✅ Option 1 — Setup Using uv (Recommended)

## 1. Install uv

### Mac / Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
### Windows
```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

# Activate the virtual Environment

## Install using uv
```bash
uv sync
```

## Or install using traditional pip
```bash
uv pip install -r requirements.txt
```

### Run Pipeline

#### Running Using UV
```bash
uv run scraper/scraper.py

uv run data/processing.py

uv run models/train.py

uv run main.py --reload
```

#### Running Using normal method
```bash
python scraper/scraper.py

python data/processing.py

python models/train.py

python main.py
```
## API runs at:
```
http://127.0.0.1:8000
```
## Interactive API docs:
```
http://127.0.0.1:8000/docs
```
