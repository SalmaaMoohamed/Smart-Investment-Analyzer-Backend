"""
main.py

ملف رئيسي لتشغيل المشروع كله:
1️⃣ تحميل البيانات من CSV
2️⃣ إضافة Features
3️⃣ (اختياري) تدريب الموديلات
4️⃣ سؤال المستخدم عن السهم والموديل
5️⃣ عمل Prediction وعرض النتيجة
"""

import token

from fastapi import FastAPI
from typing import List
import sys
from pathlib import Path
from sqlalchemy import or_
from auth.database import SessionLocal
from auth.models import User, Asset


# إضافة src للـ path
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from src.predict import predict_asset, predict_portfolio

from auth.auth import hash_password, verify_password
from auth.models import Asset
from api.enums import AssetEnum
from src.predict import predict_asset
from src.data_loader import load_asset_data
from fastapi import HTTPException, Depends
from fastapi import Header
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from api.auth_utils import create_access_token, verify_token
# from src.autho import create_access_token
# from src.autho import verify_token
from fastapi.staticfiles import StaticFiles
from scheduler import start_scheduler

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# ===== Root =====

@app.on_event("startup")
def start_background_tasks():
    start_scheduler()

@app.get("/")
def home():
    return {"message": "Welcome to the Stock Prediction API! Use /predict for single asset or /predict-portfolio for multiple assets."}

# ================= REGISTER =================

@app.post("/register")
def register(
    first_name: str,
    last_name: str,
    username: str,
    email: str,
    phone_number: str,
    password: str
):
    db = SessionLocal()

    try:
        print("🔥 Register called")

        # ===== Check email =====
        existing_email = db.query(User).filter(User.email == email).first()

        if existing_email:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

        # ===== Check username =====
        existing_username = db.query(User).filter(User.username == username).first()

        if existing_username:
            raise HTTPException(
                status_code=400,
                detail="Username already exists"
            )

        # ===== Hash Password =====
        hashed = hash_password(password)

        # ===== Create User =====
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            phone_number=phone_number,
            password=hashed
        )

        db.add(new_user)
        db.commit()

        print("✅ User added")

        return {
            "message": "User created successfully"
        }

    except HTTPException:
        raise

    except Exception as e:
        print("❌ ERROR:", e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        db.close()


# ================= LOGIN =================

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    db = SessionLocal()

    user = db.query(User).filter(
        (User.email == form_data.username) |
        (User.username == form_data.username)
    ).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({
        "user_id": user.id,
        "email": user.email
    })

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.get("/me")
def get_current_user(token: str = Depends(oauth2_scheme)):

    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    db = SessionLocal()

    user = db.query(User).filter(
        User.id == payload["user_id"]
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "email": user.email,
        "phone_number": user.phone_number
    }

@app.get("/assets")
def get_assets():
    db = SessionLocal()
    assets = db.query(Asset).all()

    result = []
    for a in assets:
        result.append({
            "id": a.id,
            "name": a.name,
            "image": a.image_url
        })

    db.close()
    return result



@app.get("/asset/{asset_id}")
def get_asset(asset_id: int):

    db = SessionLocal()

    try:
        asset = db.query(Asset).filter(
            Asset.id == asset_id
        ).first()

        if not asset:
            raise HTTPException(
                status_code=404,
                detail="Asset not found"
            )

        return {
            "id": asset.id,
            "name": asset.name,
            "symbol": asset.symbol,

            "image": f"http://127.0.0.1:8000/static/images/{asset.image_url}"
        }

    except Exception as e:

        print("❌ ERROR:", e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        db.close()

## ── Drop-in replacement for the /predict/{asset_id} endpoint in api/main.py ──
##
## Replace ONLY the @app.get("/predict/{asset_id}") function with this block.
## Everything else in main.py stays exactly the same.
##
## Changes:
##   • model_type defaults to "ensemble" (runs all models + majority vote)
##   • model_type can be overridden via query param, e.g. /predict/1?model_type=gru
##   • Response now includes a "model_type" field so the client knows what was used

@app.get("/predict/{asset_id}")
def predict(asset_id: int):

    db = SessionLocal()

    try:

        asset = db.query(Asset).filter(
            Asset.id == asset_id
        ).first()

        if not asset:
            raise HTTPException(
                status_code=404,
                detail="Asset not found"
            )

        filename = f"{asset.name}.csv"

        result = predict_asset(filename)

        return {
            "asset_id": asset.id,
            "asset_name": asset.name,

            "predicted_price": result.get("predicted_price"),

            "action": result.get("action"),

            "reasons": result.get("reasons", []),

            "model_details": result.get("model_details", {})
        }

    # ✅ مهم جدًا
    except HTTPException as e:
        raise e

    except Exception as e:

        print("❌ ERROR:", e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        db.close()

@app.get("/assets/cards")
def get_asset_cards():

    assets = {
        1: "ETEL.csv",
        2: "COMI.csv",
        3: "FWRY.csv"
    }

    result = []

    for asset_id, filename in assets.items():

        asset_name = filename.replace(".csv", "")

        df = load_asset_data(filename)

        current_price = float(df["Close"].iloc[-1])

        # ===== Prediction =====
        prediction = predict_asset(filename)

        predicted_price = prediction.get("predicted_price")
        action = prediction.get("action")

        # ===== Trend =====
        if predicted_price is not None:
            trend = "up" if predicted_price > current_price else "down"
        else:
            trend = "down"

        result.append({
            "asset_id": asset_id,

            "name": asset_name,

            "current_price": round(current_price, 2),

            "predicted_price": round(predicted_price, 2)
            if predicted_price else None,

            "action": action,

            "trend": trend,

            "logo": f"http://127.0.0.1:8000/static/images/{asset_name}.png"
        })

    return result


# ===== Predict Portfolio =====
@app.post("/predict-portfolio")
def predict_multiple(files: List[str], model_type: str = "xgboost"):
    results = predict_portfolio(files, model_type)

    return {
        "model": model_type,
        "results": results
    }


import os
import sys
from pathlib import Path
import logging
import pandas as pd

# ===== إضافة مجلد src للـ Python path =====
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from data_loader import load_all_assets
from features import add_features
from predict import predict_asset

# ===== إعداد Logging =====
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ===== ملفات البيانات =====
asset_files = ["ETEL.csv", "COMI.csv", "FWRY.csv"]

# ===== تحميل البيانات =====
logging.info("Loading assets...")
all_assets_data = load_all_assets(asset_files)


# ===== (اختياري) تدريب =====
def train_models():
    logging.info("Training XGBoost models...")
    try:
        import train_xgb
    except ImportError:
        logging.warning("train_xgb.py not found")

    logging.info("Training RL models...")
    try:
        import train_rl
    except ImportError:
        logging.warning("train_rl.py not found")