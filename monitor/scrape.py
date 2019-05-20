'''
scrape.py
---------
'''

import requests
import lxml
from lxml import html
import pandas as pd

from .exceptions import ScrapeException


class Yahoo:
    '''
    Retrieves equity data from http:://finance.yahoo.com
    '''

    URL_STRING = "http://finance.yahoo.com/quote/%s?p=%s"

    def __init__(self, symbol: str):
        self.url = self.URL_STRING % (symbol, symbol)

        try:
    `       contents = requests.get(self.url).content
        except requests.exceptions.RequestException as err:
            raise ScrapeException(err)

        html_data = html.fromstring(contents)
        table_list = html_data.xpath("//table")

        if not table_list:
            raise ScrapeException("No data for Symbol - {} on Yahoo".format(symbol))

        table_string = lxml.etree.tostring(table_list[0], method='lxml')
        price_table = pd.read_html(table_string)[0].transpose()  # Formats table
        price_table.columns = price_table.iloc[0, :]
        self.price_table = price_table.iloc[1:, :]

    def price(self) -> float:
        return float(self.price_table.loc['Close'])

    def volume(self) -> int:
        return int(self.price_table.loc['Volume'])


class Google:
    '''
    Retrieves equity data from http:://finance.google.com
    '''

    def __init__(self):
        pass

    def price(self):
        pass

    def volume(self):
        pass
