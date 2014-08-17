'''
Created on Aug 17, 2014

@author: ivan
'''
import unittest


class Test(unittest.TestCase):


    def test_load_plugins(self):
        from checker import load_plugins
        plugs=load_plugins([])
        self.assertTrue(len(plugs)>0)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_load_plugins']
    unittest.main()