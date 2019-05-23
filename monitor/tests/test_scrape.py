import pytest

from .. import scrape, exceptions


def test_yahoo_sraper():
    bad_symbol = 'RANDOM_SYMBOL'

    with pytest.raises(exceptions.ScrapeException):
        scrape.Yahoo(bad_symbol)


@pytest.fixture(scope='module')
def yahoo():
    '''
    Creates an instance of yahoo scraper for AAPL
    '''
    yahoo_symbol = 'AAPL'
    return scrape.get_scraper(yahoo_symbol, 'yahoo')


def test_price(yahoo):
    assert isinstance(yahoo.price(), float)


def test_volume(yahoo):
    assert isinstance(yahoo.volume(), int)
