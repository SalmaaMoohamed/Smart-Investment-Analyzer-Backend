# src/explainer.py

def explain_prediction(df, predicted_price, last_close):

    reasons = []

    latest = df.iloc[-1]

    # ===== RSI =====
    rsi = latest.get("RSI", 50)

    if rsi > 70:
        reasons.append({
            "en": "RSI indicates the asset may be overbought.",
            "ar": "السهم ارتفع بشكل كبير مؤخراً وقد يكون معرض لتراجع بسيط."
        })

    elif rsi < 30:
        reasons.append({
            "en": "RSI indicates the asset may be oversold.",
            "ar": "السهم منخفض بقوة مؤخراً وقد يكون قريب من الارتداد."
        })

    else:
        reasons.append({
            "en": "RSI is in a neutral range.",
            "ar": "حركة السهم حالياً مستقرة بدون ارتفاع أو هبوط مبالغ فيه."
        })

    # ===== MACD =====
    macd = latest.get("MACD", 0)

    if macd > 0:
        reasons.append({
            "en": "MACD shows bullish momentum.",
            "ar": "اتجاه السهم الحالي يميل للصعود حسب حركة السوق الأخيرة."
        })

    else:
        reasons.append({
            "en": "MACD shows bearish momentum.",
            "ar": "اتجاه السهم الحالي يميل للهبوط حسب حركة السوق الأخيرة."
        })

    # ===== Moving Average =====
    ma5 = latest.get("MA_5", last_close)
    ma20 = latest.get("MA_20", last_close)

    if ma5 > ma20:
        reasons.append({
            "en": "Short-term trend is stronger than long-term trend.",
            "ar": "الأداء قصير المدى للسهم أفضل من الأداء طويل المدى."
        })

    else:
        reasons.append({
            "en": "Long-term trend remains stronger.",
            "ar": "الاتجاه العام طويل المدى مازال أقوى."
        })

    # ===== Volatility =====
    vol = latest.get("Volatility_20", 0)

    if vol > 5:
        reasons.append({
            "en": "Market volatility is currently high.",
            "ar": "السهم حالياً متقلب بشكل كبير ونسبة المخاطرة أعلى."
        })

    else:
        reasons.append({
            "en": "Market volatility is relatively stable.",
            "ar": "حركة السهم مستقرة نسبياً ومعدل التذبذب منخفض."
        })

    # ===== AI Prediction =====
    change_percent = ((predicted_price - last_close) / last_close) * 100

    if change_percent > 2:
        reasons.append({
            "en": "AI models predict upward movement.",
            "ar": "نماذج الذكاء الاصطناعي تتوقع احتمال ارتفاع السعر."
        })

    elif change_percent < -2:
        reasons.append({
            "en": "AI models predict downward movement.",
            "ar": "نماذج الذكاء الاصطناعي تتوقع احتمال انخفاض السعر."
        })

    else:
        reasons.append({
            "en": "AI models predict sideways movement.",
            "ar": "التوقعات تشير إلى حركة عرضية بدون تغير كبير."
        })

    return reasons