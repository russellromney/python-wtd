# python-wtd
Python wrapper for World Trading Data API


### Historical data

Returns either a dict (`output='dict'`) or a DataFrame (`output='pandas'`, default )of the data. Flexible date input, optional args.

```python
from python_wtd import WTD
wtd = WTD(api_key='asdfhlaksjhdflkajsdhflkajshdflkjashdf')

my_dict = wtd.historical('AAPL',output='dict')
df = wtd.historical('AAPL',order='oldest')
df = wtd.historical('AAPL',date_from='2018',date_to=datetime.date.today())
```
Docs here: https://www.worldtradingdata.com/documentation#full-history

~~Only the historical part of the API is implemented as of v0.1.~~

### Search

Returns a list of the search results. Empty if nothing.

```python
wtd.search("AAPL",limit=1)
>>> [{'symbol': 'AAPL',
  'name': 'Apple Inc.',
  'currency': 'USD',
  'price': '210.36',
  'stock_exchange_long': 'NASDAQ Stock Exchange',
  'stock_exchange_short': 'NASDAQ'}]
```

Docs here: https://www.worldtradingdata.com/documentation#searching

~~Only historical and search are implemented as of v0.1.1.~~

### Realtime stock and mutual funds

Get real-time stock or mutual fund data as a dictionary (default) or a DataFrame.

```python
# stock
my_dict = wtd.stock('AAPL',output='dict')
df = wtd.stock(['AAPL','MSFT'])

df = wtd.mutualfund('AAAAX')
my_dict = wtd.mutualfund(['AAAAX','AAADX'],output='dict')
```

Docs here: https://www.worldtradingdata.com/documentation#real-time-market-data

 Only historical and search are implemented as of v0.1.3. Accepting all pull requests and issues.

---

Inspired by https://github.com/jamarke/pywtd/, just uses a declarative class model, allow kwargs, and aims to implement more of the API.
