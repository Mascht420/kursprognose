import pandas as pd
import numpy as np

def forecast_prices(df, interval_minutes=15, steps=96, mode="1d"):
    df = df.copy()
    df["Return"] = df["Close"].pct_change()
    last_price = df["Close"].iloc[-1]
    mean_return = df["Return"].mean()
    std_return = df["Return"].std()

    simulated_returns = np.random.normal(loc=mean_return, scale=std_return, size=steps)
    forecast_prices = [last_price]

    for r in simulated_returns:
        forecast_prices.append(forecast_prices[-1] * (1 + r))

    forecast_index = pd.date_range(start=df.index[-1], periods=steps + 1, freq=f"{interval_minutes}min")
    forecast_df = pd.DataFrame({"Forecast": forecast_prices}, index=forecast_index)
    return forecast_df
