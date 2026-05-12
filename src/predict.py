import os
import joblib
import numpy as np
import logging
from collections import Counter

from src.data_loader import load_asset_data
from src.features import add_features
from src.explainer import explain_prediction

logging.basicConfig(level=logging.INFO)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")

TIMESTEPS = 10

MODEL_WEIGHTS = {
    "xgboost": 3,
    "gru": 3,
    "lstm": 2,
    "rl": 1,
}


# ================= Helpers =================

def _get_features(df):
    return [
        col for col in df.columns
        if col not in ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    ]


def _get_action(price, last_close):
    if price is None:
        return "Hold"

    if price > last_close * 1.01:
        return "Buy"
    elif price < last_close * 0.99:
        return "Sell"
    return "Hold"


def _inverse(val, scaler):
    if scaler is None:
        return float(val)
    return float(scaler.inverse_transform([[val]])[0][0])


# ================= Model Runners =================

def _run_xgb(asset, df, cols, last_close):
    try:
        d = os.path.join(MODEL_DIR, "xgboost")

        model = joblib.load(os.path.join(d, f"{asset}_xgboost.pkl"))
        scaler_X = joblib.load(os.path.join(d, f"{asset}_scaler_X.pkl"))
        scaler_y = joblib.load(os.path.join(d, f"{asset}_scaler_y.pkl"))

        X = df[cols].iloc[-1:].values
        X = scaler_X.transform(X)

        pred = model.predict(X)[0]
        price = _inverse(pred, scaler_y)

        # 🚨 GUARDRAIL
        if abs(price - last_close) / last_close > 0.2:  # 20%
            print(f"❌ XGB rejected: {price}")
            return None, None

        return price, _get_action(price, last_close)

    except Exception as e:
        return None, None


def _run_gru(asset, df, cols, last_close):
    try:
        import tensorflow as tf

        d = os.path.join(MODEL_DIR, "gru")

        model = tf.keras.models.load_model(
            os.path.join(d, f"{asset}_gru.keras"),
            compile=False
        )

        scaler_X = joblib.load(os.path.join(d, f"{asset}_scaler_X.pkl"))
        scaler_y = joblib.load(os.path.join(d, f"{asset}_scaler_y.pkl"))

        X = df[cols].iloc[-TIMESTEPS:].values
        X = scaler_X.transform(X)
        X = X.reshape((1, TIMESTEPS, len(cols)))

        pred = model.predict(X, verbose=0)[0][0]
        price = _inverse(pred, scaler_y)

        if abs(price - last_close) / last_close > 0.2:  # 20%
            print(f"❌ GRU rejected: {price}")
            return None, None
        
        return price, _get_action(price, last_close)

    except Exception as e:
        logging.warning(f"GRU failed: {e}")
        return None, None


def _run_lstm(asset, df, cols, last_close):
    return None, None  # مش مستخدم دلوقتي


def _run_rl(asset, df, cols, last_close):
    return None, "Hold"  # action only


RUNNERS = {
    "xgboost": _run_xgb,
    "gru": _run_gru,
    "lstm": _run_lstm,
    "rl": _run_rl,
}


# ================= SMART ENSEMBLE =================

def _combine(results, last_close):
    changes = []
    votes = Counter()

    # ===== Collect normalized changes =====
    for name, (price, action) in results.items():
        w = MODEL_WEIGHTS.get(name, 1)

        if price is not None and price > 0:
            change = (price - last_close) / last_close
            changes.extend([change] * w)

        if action:
            votes[action] += w

    # ===== Filter outliers =====
    if changes:
        median = np.median(changes)

        filtered = [
            c for c in changes
            if abs(c - median) < 0.2  # 20% tolerance
        ]

        if filtered:
            final_change = float(np.mean(filtered))
        else:
            final_change = float(median)

        final_price = last_close * (1 + final_change)
    else:
        final_price = None

    # ===== Final action =====
    if votes:
        final_action = votes.most_common(1)[0][0]
    else:
        final_action = _get_action(final_price, last_close)

    return final_price, final_action


# ================= MAIN =================

def predict_asset(filename, model_type="ensemble"):
    df = load_asset_data(filename)

    if df is None:
        return None, "Hold"

    df = add_features(df)

    asset = filename.replace(".csv", "")
    cols = _get_features(df)
    last_close = float(df["Close"].iloc[-1])

    try:
        # ===== ENSEMBLE =====
        if model_type == "ensemble":
            results = {}

            for name, fn in RUNNERS.items():
                price, action = fn(asset, df, cols, last_close)
                results[name] = (price, action)

            final_price, final_action = _combine(results, last_close)

            # DEBUG (مهم جدًا دلوقتي)
            print("\n===== DEBUG =====")
            print("Last Close:", last_close)
            for k, v in results.items():
                print(k, "=>", v)
            print("FINAL:", final_price, final_action)
            print("=================\n")

            reasons = explain_prediction(df, final_price, last_close)

            return {
                "predicted_price": float(final_price) if final_price is not None else None,
                "action": final_action,
                "reasons": reasons
            }
        # ===== Single Model =====
        fn = RUNNERS.get(model_type)

        if not fn:
            return None, "Hold"

        # return fn(asset, df, cols, last_close)
    
        reasons = explain_prediction(df, price, last_close)

        return {
            "predicted_price": float(price) if price else None,
            "action": action,
            "reasons": reasons
        }

    except Exception as e:
        logging.error(f"Prediction failed: {e}")
        return None, "Hold"


def predict_portfolio(asset_files):
    results = {}

    for f in asset_files:
        price, action = predict_asset(f)
        results[f.replace(".csv", "")] = {
            "predicted_price": price,
            "action": action
        }

    return results


# ===== Run Test =====
if __name__ == "__main__":
    files = ["ETEL.csv", "COMI.csv", "FWRY.csv"]

    for f in files:
        print(f, "=>", predict_asset(f))