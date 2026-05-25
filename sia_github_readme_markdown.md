# 🚀 SIA — Smart Investment Analyzer

<div align="center">

![SIA Banner](https://img.shields.io/badge/SIA-Smart%20Investment%20Analyzer-0ea5e9?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-10b981?style=for-the-badge&logo=fastapi)
![Machine Learning](https://img.shields.io/badge/AI-Ensemble%20Models-purple?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

### 📈 AI-Powered Egyptian Stock Market Prediction System

SIA (Smart Investment Analyzer) is an intelligent stock prediction and investment analysis platform designed for the Egyptian Stock Exchange (EGX). The system combines multiple AI models, technical indicators, reinforcement learning, and market news analysis to generate smart stock predictions with human-readable explanations.

</div>

---

# ✨ Features

## 🔮 AI Stock Price Prediction
SIA predicts future stock prices using an ensemble of multiple AI models:

- ✅ XGBoost
- ✅ GRU Neural Networks
- ✅ LSTM Neural Networks
- ✅ Reinforcement Learning (DQN)
- ✅ Ensemble Decision System

---

## 📊 Technical Indicators
The system automatically calculates important financial indicators including:

- Moving Averages (MA)
- Relative Strength Index (RSI)
- MACD
- Daily Return
- Volatility

---

## 📰 AI Market Reasoning
SIA does not only predict prices.

It also explains WHY the prediction happened using:

- Financial news analysis
- Market sentiment
- Technical indicators
- Model confidence
- Trend analysis

Example:

> "The stock is predicted to rise because technical indicators show bullish momentum while recent company news sentiment is positive."

---

## 🔐 Authentication System
The backend includes a complete authentication system:

- User Registration
- Login Authentication
- JWT Access Tokens
- Persistent Login Sessions
- Protected Endpoints

---

## 📱 Mobile App Ready
The backend APIs are fully prepared to connect with a Flutter mobile application.

---

# 🧠 AI Architecture

```text
                ┌────────────────────┐
                │ Historical Stock   │
                │ Data (CSV Files)   │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Feature Engineering│
                │ RSI • MACD • MA    │
                └─────────┬──────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
   XGBoost             GRU Model        LSTM Model
        │                 │                 │
        └─────────────────┼─────────────────┘
                          ▼
                ┌────────────────────┐
                │ Ensemble Decision  │
                │ Engine             │
                └─────────┬──────────┘
                          ▼
                Predicted Price + Action
                     Buy / Sell / Hold
```

---

# 🏗️ Tech Stack

## Backend
- FastAPI
- Python 3.11
- SQLAlchemy
- SQLite
- JWT Authentication
- Uvicorn

## Machine Learning
- TensorFlow / Keras
- XGBoost
- Stable-Baselines3
- Scikit-learn
- NumPy
- Pandas

## Data Source
- Yahoo Finance API (yfinance)

---

# 📂 Project Structure

```text
Smart-Investment-Analyzer-Backend/
│
├── api/
│   └── main.py
│
├── auth/
│   ├── auth_handler.py
│   ├── database.py
│   └── models.py
│
├── data/
│   └── raw/
│       ├── ETEL.csv
│       ├── COMI.csv
│       └── FWRY.csv
│
├── models/
│   ├── xgboost/
│   ├── gru/
│   ├── lstm/
│   └── rl/
│
├── src/
│   ├── data_loader.py
│   ├── features.py
│   ├── predict.py
│   ├── train_xgb.py
│   ├── train_gru.py
│   ├── train_lstm.py
│   ├── train_rl.py
│   ├── train_all.py
│   ├── download_data.py
│   ├── sentiment_news.py
│   └── explanation_engine.py
│
├── static/
│   └── images/
│
├── app.db
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation Guide

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/SIA.git
cd SIA
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv new_env
new_env\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv new_env
source new_env/bin/activate
```

---

# 📦 Required Libraries

Install all dependencies using:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install fastapi
pip install uvicorn
pip install sqlalchemy
pip install python-jose
pip install passlib[bcrypt]
pip install python-multipart
pip install pandas
pip install numpy
pip install scikit-learn
pip install xgboost
pip install tensorflow
pip install stable-baselines3
pip install gymnasium
pip install yfinance
pip install transformers
pip install torch
pip install requests
pip install beautifulsoup4
pip install joblib
pip install matplotlib
```

---

# ▶️ Running the Server

```bash
uvicorn api.main:app --reload
```

Server URL:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 🤖 Model Training

## Train All Models

```bash
python src/train_all.py
```

## Train XGBoost Only

```bash
python src/train_xgb.py
```

## Train GRU Only

```bash
python src/train_gru.py
```

## Train LSTM Only

```bash
python src/train_lstm.py
```

## Train Reinforcement Learning Model

```bash
python src/train_rl.py
```

---

# 📥 Download Latest Stock Data

```bash
python src/download_data.py
```

---

# 📡 API Endpoints

## 🔐 Authentication

### Register

```http
POST /register
```

### Login

```http
POST /login
```

### Get Current User

```http
GET /me
```

---

## 📈 Assets

### Get Asset Details

```http
GET /asset/{asset_id}
```

### Get Assets Cards

```http
GET /assets/cards
```

---

## 🔮 Prediction

### Predict Asset

```http
GET /predict/{asset_id}
```

Returns:

```json
{
  "asset_id": 1,
  "asset_name": "ETEL",
  "predicted_price": 94.82,
  "action": "Buy",
  "reasons": [
    "Positive technical indicators",
    "Bullish market sentiment",
    "AI ensemble confidence is high"
  ]
}
```

---

# 🧪 Current Supported Stocks

| Company | Symbol |
|---|---|
| Telecom Egypt | ETEL |
| Commercial International Bank | COMI |
| Fawry | FWRY |

---

# 🔒 JWT Authentication

SIA uses JWT Bearer Tokens for secure authentication.

Token expiration:

```text
90 Days
```

Authorization Header Example:

```text
Authorization: Bearer YOUR_ACCESS_TOKEN
```

---

# 📈 Ensemble Prediction Strategy

Instead of relying on a single model, SIA combines multiple models together.

### Decision Logic

- Extreme predictions are filtered.
- Unrealistic predictions are ignored.
- The system compares predictions with the latest closing price.
- Final action is chosen based on majority voting.

This makes predictions:

- More realistic
- More stable
- More reliable

---

# 📰 News & Sentiment Analysis

SIA analyzes:

- Financial headlines
- Company news
- Market sentiment
- Bullish/Bearish language

The sentiment engine helps explain predictions in a human-friendly way.

---

# 🎨 Mobile UI Design Concept

The Flutter application includes:

- Modern investment dashboard
- Interactive stock cards
- Prediction result pages
- Trend visualization
- User profile system
- Authentication screens

Color Palette:

- Blue
- Green
- Dark Finance Theme

---

# 🚀 Future Improvements

Planned future upgrades:

- Real-time streaming prices
- Arabic NLP financial analysis
- Portfolio management
- Notifications system
- AI chatbot assistant
- Advanced candlestick charts
- Cloud deployment
- PostgreSQL migration

---

# 👩‍💻 Developed By

### Salmaa Mohamed

AI & Backend Developer — Smart Investment Analyzer (SIA)

---

# ⭐ Why SIA is Different

Unlike traditional stock prediction systems, SIA:

✅ Uses multiple AI models together

✅ Explains prediction reasons

✅ Analyzes market sentiment

✅ Supports mobile integration

✅ Focuses on Egyptian Stock Market

✅ Combines AI + Financial Analysis + Reinforcement Learning

---

# 📜 License

This project is for educational and research purposes.

---

# ❤️ Final Note

SIA is more than just a stock predictor.

It is an intelligent financial assistant designed to help users understand market behavior using Artificial Intelligence.

---

<div align="center">

# 🚀 Smart Investment Analyzer (SIA)
### Predict Smarter • Invest Better

</div>

