import yfinance as yf
import requests

# ---------- TELEGRAM DETAILS ----------
BOT_TOKEN = "YAHAN_TUMHARA_BOT_TOKEN"
CHAT_ID = "YAHAN_TUMHARA_CHAT_ID"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data)

# ---------- DATA DOWNLOAD ----------
symbol = "^NSEI"
data = yf.download(tickers=symbol, interval="5m", period="1d")

if data.empty:
    send_telegram("⚠️ Data empty, market closed or issue")
    exit()

last_50 = data.tail(50)

highs = last_50['High'].dropna().values
lows  = last_50['Low'].dropna().values

higher_high = sum(highs[i] > highs[i-1] for i in range(1, len(highs)))
higher_low  = sum(lows[i] > lows[i-1] for i in range(1, len(lows)))

# ---------- TREND ----------
if higher_high > 30 and higher_low > 30:
    trend = "UP"
elif higher_high < 20 and higher_low < 20:
    trend = "DOWN"
else:
    trend = "SIDEWAYS"

# ---------- LAST CANDLE ----------
last = data.iloc[-1]
open_ = float(last['Open'])
high  = float(last['High'])
low   = float(last['Low'])
close = float(last['Close'])

body = abs(close - open_)
upper_wick = high - max(open_, close)
lower_wick = min(open_, close) - low

signal = "NO TRADE"

if trend == "UP" and lower_wick > body * 1.5:
    signal = "🟢 BUY SIGNAL"

elif trend == "DOWN" and upper_wick > body * 1.5:
    signal = "🔴 SELL SIGNAL"

# ---------- MESSAGE ----------
if signal != "NO TRADE":
    send_telegram(
        f"{signal}\n"
        f"Trend: {trend}\n"
        f"Open: {open_}\nClose: {close}"
    )
