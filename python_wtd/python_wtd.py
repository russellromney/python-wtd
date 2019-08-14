import requests
from dateutil.parser import parse
import pandas as pd
from datetime import datetime

class WTDException(Exception):
    pass

class WTD:
    '''
    Simple class to pull data from the World Trading Data into Pandas DataFrames.
    '''
    def __init__(self,api_key=''):
        self.api_key = api_key
        self.API = 'https://www.worldtradingdata.com/api/v1'

    def _confirm(self):
        if self.api_key=='':
            return WTDException('No API key specified')
    
    def historical(self,ticker,**kwargs):
        '''
        get historical data for <ticker> or each stock in <ticker> with args
        '''
        self._confirm()

        params = {
            'symbol':ticker,
            'api_token':self.api_key,
            **kwargs
        }
        if params.get('date_from',0):
            params['date_from'] = self._date(params['date_from'])
        if params.get('date_to',0):
            params['date_to'] = self._date(params['date_to'])

        r = requests.get(self.API + '/history', params=params)
        data = r.json()
        df = pd.DataFrame.from_dict(data['history'], orient='index')
        df.index = pd.to_datetime(df.index)
        df = df.apply(pd.to_numeric)
        return df


    def _date(self,date_):
        if isinstance(date_, datetime) or isinstance(date_,pd.Timestamp):
            return date_.strftime('%Y-%m-%d')
        elif isinstance(date_, str):
            return parse(date_).strftime('%Y-%m-%d')
        else:
            raise WTDException('Invalid date')

    
    