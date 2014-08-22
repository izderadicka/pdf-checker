#! /usr/bin/env python
'''
Created on Aug 20, 2014

@author: ivan
'''
from gevent import monkey
monkey.patch_all()

from server import app as application

if __name__=='__main__':
    from gevent import pywsgi
    import argparse
    p= argparse.ArgumentParser()
    p.add_argument('-a', '--address', default='127.0.0.1', help='ip address to listen to')
    p.add_argument('-p', '--port', default=8000, help='port to listen to')
    args=p.parse_args()
    server = pywsgi.WSGIServer((args.address, args.port), application)
    server.serve_forever()