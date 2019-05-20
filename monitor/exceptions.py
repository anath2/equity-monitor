'''
Exception classes for the package
'''


class EquityMonitorException(Exception):
    '''
    Base class for all EquityMonitor exceptions
    '''


class ScrapeException(EquityMonitorException):
    '''
    Exception is thrown when an error occurs scraping
    financial data
    '''