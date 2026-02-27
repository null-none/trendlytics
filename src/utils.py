import pandas as pd
import yfinance as yf
from datetime import datetime


class TrendCalculator:
    def __init__(self, ticker="BTC-USD", sma_window=20, ema_window=20):
        self.ticker = ticker
        self.sma_window = sma_window
        self.ema_window = ema_window
        self.data = None
        self.latest_result = None

    def download_data(self, start="2022-01-01"):
        end = datetime.today().strftime("%Y-%m-%d")
        raw = yf.download(
            self.ticker, start=start, end=end, interval="1d", progress=False
        )
        if raw.empty:
            raise ValueError(f"No data returned by yfinance for ticker '{self.ticker}'")
        if isinstance(raw.columns, pd.MultiIndex):
            raw.columns = raw.columns.get_level_values(0)
        close = raw[["Close"]].squeeze()
        df = close.to_frame("price")
        df.index.name = "date"
        df.reset_index(inplace=True)
        self.data = df

    def calculate_trends(self):
        df = self.data.copy()
        df["price"] = df["price"].squeeze()
        df["SMA"] = df["price"].rolling(window=self.sma_window).mean()
        df["EMA"] = df["price"].ewm(span=self.ema_window, adjust=False).mean()

        df["signal"] = 0
        df.loc[df["EMA"] > df["SMA"], "signal"] = 1  # BUY
        df.loc[df["EMA"] < df["SMA"], "signal"] = -1  # SELL

        self.data = df.dropna()

        latest = self.data.iloc[-1]
        self.latest_result = {
            "date": latest["date"].strftime("%Y-%m-%d"),
            "price": round(float(latest["price"]), 2),
            "sma": round(float(latest["SMA"]), 2),
            "ema": round(float(latest["EMA"]), 2),
            "signal": int(latest["signal"]),
        }

    def calculate(self, start="2022-01-01"):
        self.download_data(start)
        self.calculate_trends()

    def get_latest_json(self):
        return self.latest_result

    def get_data(self):
        return self.data
