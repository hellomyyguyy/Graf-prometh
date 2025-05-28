from flask import Flask, Response
from prometheus_client import Gauge, generate_latest, CollectorRegistry
import requests

app = Flask(__name__)
registry = CollectorRegistry()
btc_price_gauge = Gauge('btc_price_usd', 'Current BTC price in USD', registry=registry)

def fetch_btc_price():
    try:
        res = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot", timeout=5)
        res.raise_for_status()
        return float(res.json()['data']['amount'])
    except Exception as e:
        print(f"[ERROR] {e}")
        return None

@app.route("/metrics")
def metrics():
    price = fetch_btc_price()
    if price:
        btc_price_gauge.set(price)
    return Response(generate_latest(registry), mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
