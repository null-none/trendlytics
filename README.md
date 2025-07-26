# TrendLytics

TrendLytics is a lightweight Python library for calculating SMA, EMA, and basic trading signals on crypto assets like Bitcoin. Returns clean JSON output for easy integration. 

```python
from trendlytics.utils import TrendCalculator

trend = TrendCalculator(ticker="BTC-USD", sma_window=20, ema_window=20)
trend.calculate(start="2023-01-01")
print(trend.get_latest_json())

```

```bash
{
  "date": "2025-07-24",
  "price": 61200.55,
  "SMA": 60555.42,
  "EMA": 61022.75,
  "signal": "BUY"
}
```