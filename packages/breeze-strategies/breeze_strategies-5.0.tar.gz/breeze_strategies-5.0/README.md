# LIVE  python_strategies

## Steps to install Strategy Library for LIVE


```python

pip install breeze_strategies==5.0

```


## code usage

```python

from breeze_strategies import Strategies


obj = Strategies(app_key = "your app key",secret_key = "your secret key",api_session = "your api session",max_profit = "your max profit",max_loss = "your max loss")
obj.long_straddle(stock_code = "NIFTY",strike_price = "18700",qty = "50",expiry_date = "2023-06-15T06:00:00.000Z")
obj.stop()
obj.get_pnl()
obj.squareoff(exchange_code = "exchange_code", stock_code = "stock_code", product_type = "product_type", expiry_date = "expiry_date", strike_price = "strike_price", action = "buy", order_type = "market" , validity = "validity", stoploss, quantity = "quantity" , price = "executed price",validity_date = "validity_date", trade_password = "", disclosed_quantity = "0",right = "Call")



```

