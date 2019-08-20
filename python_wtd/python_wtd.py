import requests
from dateutil.parser import parse
import pandas as pd
from datetime import datetime
import functools


class WTD(object):
    '''
    Simple class to pull data from the World Trading Data into Pandas DataFrames.
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



    @WTDDecorators.confirm_api_key
    def historical(self,ticker,**kwargs):
        '''
        get historical data for <ticker> or each stock in <ticker> with args
        '''
        # ensure date params are correct
        params = self._process_date_params(
            {
                'symbol':ticker,
                'api_token':self.api_key,
                **kwargs
            }
        )

        r = requests.get(self.API + '/history', params=params)
        data = r.json()
        df = pd.DataFrame.from_dict(data['history'], orient='index')
        df.index = pd.to_datetime(df.index)
        df = df.apply(pd.to_numeric)
        return df


    @WTDDecorators.confirm_api_key
    def search(self,search_term,**kwargs):
        '''
        return the seach results for the search phrase with any other parameters
        '''
        # ensure date params are correct
        params = self.process_date_params(
            {
                'search_term':search_term,
                'api_token':self.api_key,
                **kwargs
            }
        )

        r = requests.get(self.API + '/stock_search', params=params)

        data = r.json()
        data = data['data']

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
