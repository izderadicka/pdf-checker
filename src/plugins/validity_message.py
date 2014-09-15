'''
Created on Sep 15, 2014

@author: ivan
'''

from forbidden_words import ForbiddenWords

def create_instance():
    i= ForbiddenWords(['This Ordering Document must be executed by you and Oracle on or before'])
    i.change_name('Quote Validity Language Check')
    return i