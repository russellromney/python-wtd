# python-wtd
Python wrapper for World Trading Data API

---

Returns a Pandas DataFrame of the data. Flexible date input, optional args. Some error checking before the API request.

**Historical data**

```python
from python_wtd import WTD
wtd = WTD(api_key='asdfhlaksjhdflkajsdhflkajshdflkjashdf')

df = wtd.historical('AAPL')
df = wtd.historical('AAPL',order='oldest')
df = wtd.historical('AAPL',date_from='2018')
df = wtd.historical('AAPL',date_to=datetime.date.today())
```

~~Only the historical part of the API is implemented as of v0.1.~~

**Search**

```python
wtd.search("AAPL",limit=2)
>>> [{'symbol': 'AAPL',
  'name': 'Apple Inc.',
  'currency': 'USD',
  'price': '210.36',
  'stock_exchange_long': 'NASDAQ Stock Exchange',
  'stock_exchange_short': 'NASDAQ'},
 {'symbol': 'AAPL.BA',
  'name': 'APPLE INC CEDEAR',
  'currency': 'ARS',
  'price': '1172.00',
  'stock_exchange_long': 'Buenos Aires Stock Exchange',
  'stock_exchange_short': 'BCBA'}]
```

Only historical and search are implemented as of v0.1.1. Accepting all pull requests and issues.

---

Inspired by https://github.com/jamarke/pywtd/, just uses a declarative class model, allow kwargs, and aims to implement more of the API.
