import requests
from dateutil.parser import parse
import pandas as pd
from datetime import datetime
import functools
from io import StringIO

class WTD(object):
    '''
    Simple class to pull data from the World Trading Data into preferred data structure.
    '''
    class WTDException(Exception):
        pass

    class WTDDecorators(object):
        '''holds decorators for python-wtd'''

        @classmethod
        def confirm_api_key(cls,f):
            '''
            confirms that the given api key is at least not in ['',None]
            '''
            @functools.wraps(f)
            def decorated_function(*args,**kwargs):
                if args[0].api_key in ['',None]:
                    raise WTD.WTDException('No API key specified')
                return f(*args,**kwargs)
            return decorated_function


    def __init__(self,api_key=''):
        self.api_key = api_key
        self.API = 'https://www.worldtradingdata.com/api/v1'


    # historical
    @WTDDecorators.confirm_api_key
    def historical(self,ticker,output='pandas',**kwargs):
        '''
        get historical data for <ticker> or each stock in <ticker> with args

        if output is 'pandas', returns DataFrame of output
        if output is 'dict', returns a dictionary representation of the data

        other parameters:
            sort:
                'newest', 'oldest', 'desc', 'asc'
            date_from:
            date_to
            formatted:
                'true','false' (def False)
        '''
        if not output in ['dict','pandas']:
            raise WTDException('WTD.historical: output must be one of "pandas","dict"')

        # ensure date params are correct
        #params = self._process_date_params(
        {
            'symbol':ticker,
            'api_token':wtd.api_key,
            # **kwargs
        }
        #)

        data = requests.get(wtd.API + '/history', params=params)
        data = data.json()
        data = data['history']

        if output=='dict':
            pass
        else:
            data = pd.DataFrame.from_dict(data, orient='index')
            data.index = pd.to_datetime(data.index)
            data = data.apply(pd.to_numeric)

        return data

    # search
    @WTDDecorators.confirm_api_key
    def search(self,search_term,**kwargs):
        '''
        return a dict of seach results for the search phrase with any other parameters

        search_term must be a string

        Other parameters:
            stock_exchange
            currency
            limit
            page
            sort_by:
                'symbol', 'name', 'currency',
                'stock_exchange_long', 'stock_exchange_short',
                'market_cap', 'volume', 'change_pct'
            sort_order:
                'asc','desc'
        '''
        if not isinstance(search_term,str):
            raise WTDException('WTD.search: search_term must be of type str')

        params = {
                'search_term':search_term,
                'api_token':self.api_key,
                **kwargs
            }
        )

        r = requests.get(self.API + '/stock_search', params=params)

        data = r.json()
        data = data['data']

        return data

    # realtime stock
    @WTDDecorators.confirm_api_key
    def stock(ticker,output='dict',**kwargs):
        '''
        return the realtime market for a stock or an iterable of stocks

        ticker can be a string or an iterable

        if output is 'pandas', returns a DataFrame of results
        if output is 'dict', returns a list of dicts (default)

        other parameters:
            sort_order:
                'desc', 'asc'
            sort_by:
                'symbol', 'name', 'list_order'
        '''
        if not output in ['pandas','dict']:
            raise WTDException('WTD.stock: output must be one of "pandas","dict"')

        if isinstance(ticker,str):
            pass
        else:
            try:
                ticker = [x for x in ticker]
                assert len(ticker)>0
                assert all( [ isinstance(x,str) for x in ticker] )
                ticker = ','.join(ticker)
            except:
                raise WTD.WTDException('WTD.stock: ticker must be a string or a list/tuple of strings')

        params = {
            'api_token':wtd.api_key,
            'output':{'pandas':'csv','dict':'json'}[output],
            'symbol':ticker
        }
        url = wtd.API+'/stock'

        if output=='pandas':
            with requests.Session() as s:
                 data = s.get(url,params=params)
                 data = data.content.decode('utf-8')
                 data = pd.read_csv(StringIO(data))
        else: # output = 'dict'
            data = requests.get(url,params=params)
            data = data.json()

        return data


    # realtime mutual fund
    @WTDDecorators.confirm_api_key
    def mutualfund(ticker,output='dict',**kwargs):
        '''
        return the realtime data for a stock or an iterable of stocks

        ticker can be a string or an iterable

        if output is 'pandas', returns a DataFrame of results
        if output is 'dict', returns a list of dicts (default)

        other parameters:
            sort_order:
                'desc', 'asc'
            sort_by:
                'symbol', 'name', 'list_order'
        '''
        if not output in ['pandas','dict']:
            raise WTDException('WTD.stock: output must be one of "pandas","dict"')

        if isinstance(ticker,str):
            pass
        else:
            try:
                ticker = [x for x in ticker]
                assert len(ticker)>0
                assert all( [ isinstance(x,str) for x in ticker] )
                ticker = ','.join(ticker)
            except:
                raise WTD.WTDException('WTD.stock: ticker must be a string or a list/tuple of strings')

        params = {
            'api_token':wtd.api_key,
            'output':{'pandas':'csv','dict':'json'}[output],
            'symbol':ticker
        }
        url = wtd.API+'/mutualfund'

        if output=='pandas':
            with requests.Session() as s:
                 data = s.get(url,params=params)
                 data = data.content.decode('utf-8')
                 data = pd.read_csv(StringIO(data))
        else: # output = 'dict'
            data = requests.get(url,params=params)
            data = data.json()

        return data



    def process_date(self,date_):
        '''
        turn some date string or object into a date string
        '''
        if isinstance(date_, datetime) or isinstance(date_,pd.Timestamp):
            return date_.strftime('%Y-%m-%d')
        elif isinstance(date_, str):
            return parse(date_).strftime('%Y-%m-%d')
        else:
            raise WTDException('Invalid date')


    def process_date_params(self,params):
        '''
        change date_from and date_to params to strings if they exist
        then return params
        '''
        if params.get('date_from',0):
            params['date_from'] = self.process_date(params['date_from'])
        if params.get('date_to',0):
            params['date_to'] = self.process_date(params['date_to'])

        return params
