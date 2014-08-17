'''
Created on Aug 17, 2014

@author: ivan
'''

from plugins.numbering_check import NumberingCheck


def create_instance():
    i=NumberingCheck(max_left=5)
    i.change_name(i.name+" modified")
    return i