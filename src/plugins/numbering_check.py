'''
Created on Aug 17, 2014

@author: ivan
'''

import re
from common import CheckStrategy

class NumberingCheck(CheckStrategy):
    name="Numbering Check"
    def __init__(self, max_left=10,
                 l1_re=r'^([A-Z])\.\s+.{3,}',
                 l2_re=r'^(\d+)\.\s+.{3,}',
                 l3_re=r'^([a-z])\.\s+.{3,}',
                 start_values=['A','1', 'a']):
        super(NumberingCheck,self).__init__()
        self.max_left=max_left
        self.l1_re=re.compile(l1_re)
        self.l2_re=re.compile(l2_re)
        self.l3_re=re.compile(l3_re)
        self.l1=None
        self.l2=None
        self.l3=None
        self.start_values=start_values
    
    def _add_error(self, level, curr, next, txt):
        self.results.add_problem("Level %d wrong numbering, is %s, but should be %s" %
                           (level,curr, next),txt)
        
    def _next_item(self, r, level, next_fn):
        curr=getattr(self, "l%d"%level)
        if curr is None:
            next=self.start_values[level-1]
        else:
            next=next_fn(curr) 
        setattr(self, "l%d"%level, next)
        item=r.group(1)
        return item == next, item, next
    
    def _next_letter(self,r,level):
        return self._next_item(r, level, lambda curr: chr(ord(curr)+1))
    def _next_number(self,r,level):
        return self._next_item(r, level, lambda curr: str(int(curr)+1))
        
    def feed(self, txt):
        if txt.left <= self.max_left:
            l3=self.l3_re.match(txt.text)
            if l3:
                ok,curr,next = self._next_letter(l3,3)
                if not ok:
                    self._add_error(3, curr, next, txt)
            else:
                l2=self.l2_re.match(txt.text)
                if l2:
                    ok,curr,next = self._next_number(l2,2)
                    if not ok:
                        self._add_error(2, curr, next, txt)
                    self.l3=None
                else:
                    l1=self.l1_re.match(txt.text)
                    if l1:
                        ok,curr,next = self._next_letter(l1,1)
                        if not ok:
                            self._add_error(1, curr, next, txt)
                        self.l2=None
                        self.l3=None