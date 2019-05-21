#!/usr/bin/python
# coding:utf-8
# Copyright (C) 2005-2019 All rights reserved.
# FILENAME: 	  simple_http_client.py
# VERSION: 	    1.0
# CREATED: 	    2019-05-21 10:21
# AUTHOR: 	    Aekasitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
'''
Module defining SimpleHttpClient class
'''
import sys
import json
import importlib
import http.client as httplib
from urllib.parse import urlencode
from _socket import error as SocketError
importlib.reload(sys)

class SimpleHttpClient(object):
    '''
    Simple Client defined used to get standardised response of HTTP requests
    Only has two request types: [GET, POST]
    '''

    def __init__(self, endpoint, secure=False):
        self.endpoint = endpoint
        self.secure = secure

    def __get_conn(self):
        if self.endpoint is not None:
            if self.secure:
                return httplib.HTTPSConnection(self.endpoint)
            else:
                return httplib.HTTPConnection(self.endpoint)

    def get(self, route='/', queries=None):
        """Create a GET Request with given route and queries, return response"""
        conn = self.__get_conn()
        if conn is None: raise SimpleHttpException('Connection Cannot Be Created.')
        if queries:
            route += '?' + urlencode(queries)
        try:
            conn.request('GET', route)
            res = conn.getresponse()
            content = res.read()
            conn.close()
            if res.status == httplib.OK:
                if res.getheader('content-type') == 'application/json':
                    return json.loads(content) 
                return content
            elif res.status in [httplib.CREATED, httplib.ACCEPTED]:
                pass
            elif res.status == httplib.UNAUTHORIZED:
                raise Unauthorized(content)
            elif res.status == httplib.BAD_REQUEST:
                raise BadRequest(content)
            elif res.status == httplib.INTERNAL_SERVER_ERROR:
                raise InternalServerError(content)
            else:
                pass
        except (httplib.BadStatusLine, SocketError) as err:
            raise SimpleHttpException(err)

    def post(self, route='/', queries=None, payload=None):
        """Create a POST Request with given route and queries, return response"""
        conn = self.__get_conn()
        if conn is None: raise SimpleHttpException('Connection Cannot Be Created.')
        if queries:
            route += '?' + urlencode(queries)
        try:
            if payload is not None and isinstance(payload, dict):
                conn.request('POST', route, body=json.dumps(payload), headers={
                'Content-Type': 'application/json'
            })
            else:
                conn.request('POST', route)
            res = conn.getresponse()
            content = res.read()
            conn.close()
            if res.status == httplib.OK:
                if res.getheader('content-type') == 'application/json':
                    return json.loads(content)
                return content
            if res.status in [httplib.CREATED, httplib.ACCEPTED]:
                pass
            elif res.status == httplib.UNAUTHORIZED:
                raise Unauthorized(content)
            elif res.status == httplib.BAD_REQUEST:
                raise BadRequest(content)
            elif res.status == httplib.INTERNAL_SERVER_ERROR:
                raise InternalServerError(content)
            else:
                pass
            conn.close()
        except (httplib.BadStatusLine, SocketError) as err:
            raise SimpleHttpException(err)

########################################
##             Exceptions             ##
########################################
class SimpleHttpException(httplib.HTTPException): pass
class Unauthorized(SimpleHttpException): pass
class BadRequest(SimpleHttpException): pass
class InternalServerError(SimpleHttpException): pass
