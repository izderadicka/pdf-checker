'''
Created on Aug 20, 2014

@author: ivan
'''
from gevent import monkey
monkey.patch_all()

from server import app as application