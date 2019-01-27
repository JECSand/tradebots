"""
==========================================
TradeBots
Version: 0.0.1
Request Utility Functions
==========================================

Authors: Connor Sanders
"""

import sys
import json
import time
if sys.version_info < (3, 0, 0):
    from urllib2 import Request, urlopen
else:
    from urllib.request import Request, urlopen


# Function to handle a get request
def base_request(url, req_type, headers, req_data=None):
    if req_type != 'GET' and req_data is not None:
        req = Request(url, data=json.dumps(req_data).encode('utf8'))
    else:
        req = Request(url)
    if headers is not None:
        for header_key, header_val in headers.items():
            req.add_header(header_key, header_val)
    if req_type != 'GET':
        req.get_method = lambda: req_type
    return urlopen(req)


# Function to handle a new request
def handle_request(url, req_type, headers, req_data=None, i=0):
    if i == 4:
       return None
    try:
        if req_data is None:
            res = base_request(url, req_type, headers)
        else:
            res = base_request(url, req_type, headers, req_data)
        if res.code == 500:
            i += 1
            return handle_request(url, req_type, headers, req_data, i)
        else:
            return res
    except:
        i += 1
        return handle_request(url, req_type, headers, req_data, i)


# Function to handle a get request
def get_request(url, headers=None):
    return handle_request(url, 'GET', headers)


# Function to handle a post request
def post_request(url, req_data, headers=None):
    return handle_request(url, 'POST', headers, req_data)


# Function to handle a put request
def put_request(url, req_data, headers=None):
    return handle_request(url, 'PUT', headers, req_data)


# Function to handle a put request
def patch_request(url, req_data, headers=None):
    return handle_request(url, 'PATCH', headers, req_data)


# Function to handle a delete request
def delete_request(url, headers=None):
    return handle_request(url, 'DELETE', headers)
