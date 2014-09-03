# coding=utf-8
'''
Created on Aug 17, 2014

@author: ivan
'''

import re
from common import CheckStrategy

class NumberingCheck(CheckStrategy):
    name="Numbering Check"
    section_headers=[u"License Definitions and Rules",
                     u"Lizenzdefinitionen und Regeln",
                     u"Définitions Licence et Règles Tarifaires",
                     u"Definicje i zasady udzielania licencji",
                     u"Licencne definicije i pravila"]
    def __init__(self, max_left=10,
                 l1_re=r'^([A-Z])\.\s+.{3,}',
                 l2_re=r'^(\d+)\.\s+.{3,}',
                 l3_re=r'^([a-z])\.\s+.{3,}',
                 start_values=['A','1', 'a'],
                 min_font_size=[8,8,0]):
        super(NumberingCheck,self).__init__()
        self.max_left=max_left
        self.l1_re=re.compile(l1_re)
        self.l2_re=re.compile(l2_re)
        self.l3_re=re.compile(l3_re)
        self.l1=None
        self.l2=None
        self.l3=None
        self.start_values=start_values
        self.min_font_size=min_font_size
    
    def _add_error(self, level, curr, next, txt):
        self.results.add("Level %d wrong numbering, is %s, but should be %s" %
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
    def _is_new_section(self, text):
        for h in self.section_headers:
            if re.search(u'^'+h, text, re.UNICODE|re.IGNORECASE):
                return True   
    def _has_min_size(self,txt, level): 
        return txt.font_size>= self.min_font_size[level-1]
    def feed(self, txt):
        if self._is_new_section(txt.text):
            self.l1=None
            self.l2=None
            self.l3=None
        elif txt.left <= self.max_left:
            l3=self.l3_re.match(txt.text)
            if l3 and self._has_min_size(txt, 3):
                ok,curr,next = self._next_letter(l3,3)
                if not ok:
                    self._add_error(3, curr, next, txt)
            else:
                l2=self.l2_re.match(txt.text)
                if l2 and self._has_min_size(txt, 2):
                    ok,curr,next = self._next_number(l2,2)
                    if not ok:
                        self._add_error(2, curr, next, txt)
                    self.l3=None
                else:
                    l1=self.l1_re.match(txt.text)
                    if l1 and self._has_min_size(txt, 1):
                        ok,curr,next = self._next_letter(l1,1)
                        if not ok:
                            self._add_error(1, curr, next, txt)
                        self.l2=None
                        self.l3=None