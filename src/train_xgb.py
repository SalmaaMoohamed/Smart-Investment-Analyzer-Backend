import sys
import os
import joblib
import pandas as pd

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_loader import load_all_assets
from features import add_features

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from xgboost import XGBRegressor


# ===== Paths =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))

MODEL_DIR = os.path.join(PROJECT_ROOT, "models", "xgboost")
os.makedirs(MODEL_DIR, exist_ok=True)

asset_files = ["ETEL.csv", "COMI.csv", "FWRY.csv"]


def train_xgb():
    all_assets = load_all_assets(asset_files)

    for asset_name, df in all_assets.items():
        print(f"\n📊 Training XGBoost for {asset_name}...")

        df = add_features(df)

        # ===== Features =====
        feature_cols = [
            col for col in df.columns
            if col not in ['Date', 'Close']
        ]

        X = df[feature_cols].values
        y = df['Close'].values.reshape(-1, 1)

        # ===== Scaling =====
        scaler_X = MinMaxScaler()
        X_scaled = scaler_X.fit_transform(X)

        scaler_y = MinMaxScaler()
        y_scaled = scaler_y.fit_transform(y)

        # ===== Split =====
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y_scaled, test_size=0.2, shuffle=False
        )

        # ===== Model =====
        model = XGBRegressor(
            n_estimators=300,
            learning_rate=0.05,
            max_depth=5
        )

        model.fit(X_train, y_train.ravel())

        # ===== Evaluate =====
        pred_scaled = model.predict(X_test).reshape(-1, 1)
        pred_real = scaler_y.inverse_transform(pred_scaled)
        y_real = scaler_y.inverse_transform(y_test)

        mse = mean_squared_error(y_real, pred_real)
        print(f"✅ MSE: {mse:.4f}")

        # ===== Save everything =====
        joblib.dump(model, os.path.join(MODEL_DIR, f"{asset_name}_xgboost.pkl"))
        joblib.dump(scaler_X, os.path.join(MODEL_DIR, f"{asset_name}_scaler_X.pkl"))
        joblib.dump(scaler_y, os.path.join(MODEL_DIR, f"{asset_name}_scaler_y.pkl"))
        joblib.dump(feature_cols, os.path.join(MODEL_DIR, f"{asset_name}_features.pkl"))

        print(f"💾 Saved model for {asset_name}")


if __name__ == "__main__":
    train_xgb()