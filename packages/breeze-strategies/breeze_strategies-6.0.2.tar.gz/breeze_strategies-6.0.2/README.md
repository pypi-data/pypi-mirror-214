# LIVE  python_strategies

## Steps to install Strategy Library for LIVE


```python

pip install breeze_strategies==6.0.2

```


## code usage

```python

from breeze_strategies import Strategies


obj = Strategies(app_key = "your app key",secret_key = "your secret key",api_session = "your api session",max_profit = "your max profit",max_loss = "your max loss")
obj.long_straddle(stock_code = "NIFTY",strike_price = "18700",qty = "50",expiry_date = "2023-06-15T06:00:00.000Z")
obj.stop() #for disconnection and exit of current strategy
obj.get_pnl()

```

