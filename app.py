from flask import Flask, request, jsonify
import requests, os

app = Flask(__name__)

PROVIDER = "coingecko"   # أو coinmarketcap

def fetch_prices(ids):
    if PROVIDER == "coingecko":
        url = "https://api.coingecko.com/api/v3/simple/price"
        r = requests.get(url, params={"ids": ",".join(ids), "vs_currencies": "usd"})
        return {k.upper(): v["usd"] for k, v in r.json().items()}
    else:  # CoinMarketCap
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        headers = {"X-CMC_PRO_API_KEY": os.getenv("CMC_KEY")}
        r = requests.get(url, headers=headers, params={"symbol": ",".join([i.upper() for i in ids])})
        data = r.json()["data"]
        return {sym: data[sym]["quote"]["USD"]["price"] for sym in data}

@app.route("/prices")
def all_prices():
    symbols = request.args.get("symbols", "bitcoin,ethereum").lower().split(",")
    prices = fetch_prices(symbols)
    return jsonify(prices)

if __name__ == "__main__":
    app.run()