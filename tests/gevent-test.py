'''
Created on Aug 20, 2014

@author: ivan
'''

import time




def application(e, sr):
    path = e.get('PATH_INFO', '')
    if path=='' or path=='/':
        sr('200 OK', [('Content-Type','text/html')])
        yield "sleeping for 30 seconds...<br/>\n"
        time.sleep(30)
        yield "done<br>\n"
    else:
        sr('404 Not Found', [('Content-Type','text/html')])
        yield "Not found"
    
if __name__=='__main__':
    from gevent import pywsgi
    server = pywsgi.WSGIServer(('127.0.0.1', 8000), application)
    server.serve_forever()
   