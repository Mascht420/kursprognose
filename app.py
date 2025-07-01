from flask import Flask, render_template, request
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
from forecast import forecast_prices

app = Flask(__name__)

SYMBOLS = {
    "SPY": "SPY",
    "DAX": "^GDAXI",
    "MSFT": "MSFT",
    "AAPL": "AAPL"
}

@app.route("/", methods=["GET", "POST"])
def index():
    selected = "SPY"
    chart_json = None
    forecast_mode = None

    if request.method == "POST":
        selected = request.form.get("symbol")
        forecast_mode = request.form.get("forecast")

        symbol = SYMBOLS.get(selected, "SPY")
        df = yf.Ticker(symbol).history(period="5d", interval="15m")

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df["Close"], mode="lines", name="Kurs"))

        if forecast_mode:
            steps = 96 if forecast_mode == "1d" else 96 * 5
            forecast_df = forecast_prices(df, interval_minutes=15, steps=steps, mode=forecast_mode)
            fig.add_trace(go.Scatter(x=forecast_df.index, y=forecast_df["Forecast"], mode="lines", name="Prognose"))

        fig.update_layout(title=f"{selected} Kurs & Prognose", xaxis_title="Zeit", yaxis_title="Kurs", height=600)
        chart_json = fig.to_json()

    return render_template("index.html", chart_json=chart_json, selected=selected)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
