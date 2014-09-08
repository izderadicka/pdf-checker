'''
Created on Sep 2, 2014

@author: ivan
'''

from collections import deque
import re
from common import CheckStrategy
from checker import TextLine

class FooterCheck(CheckStrategy):
    name="Page Footer Check"
    
    def __init__(self):
        super(FooterCheck,self).__init__()
        self._curr_page=None
        self.footers=[]
        
        
    def feed(self, txt):
        pg=txt.page_no
        if pg != self._curr_page:
            self.footers.append(deque(maxlen=self.FOOTER_MAX))
            self._curr_page=pg
            
        if txt.top >= 90.5:
            self.footers[pg-1].appendleft(txt)
            
    
    FOOTER_MAX=4
    PAGE_FOOTER=0
    PG_RE=re.compile(r'^\w+\s+(\d+)\s+\w+\s+(\d+)$', re.UNICODE)  
    QUOTE_RE=re.compile(u'^[\\d]+\\s*[-\u2010\u2011\u2012\u2013\u2014\u2015]\\s*[\\d]+$', re.UNICODE)
    def prepare_results(self):
        pg_count=self._curr_page
        for i in xrange(len(self.footers)):
            if i==0:
                vals=map(lambda v: v.text, self.footers[i])
                while len(vals) and not self.QUOTE_RE.match(vals[-1])  :
                    vals.pop()
                if not len(vals):
                    self.results.add_unplaced("Footer is missing quote number" ,
                                             page=1, top=91)
            else:
                for j in xrange(len(vals)):
                    if j != self.PAGE_FOOTER:
                        try:
                            if self.footers[i][j].text != vals[j]:
                                self.results.add("Footer is different from page 1 '%s'"% vals[j],
                                                 self.footers[i][j] )
                        except IndexError:
                            self.results.add_unplaced("Footer has incorrect number of items %d" % len(self.footers[i]),
                                             page=i-1, top=91)
            paging=self.footers[i][self.PAGE_FOOTER]
            m=self.PG_RE.match(paging.text)
            if m:
                pg, tot=int(m.group(1)), int(m.group(2))
                if pg != i+1 or tot!= pg_count:
                    self.results.add("Page count is wrong is %d/%d but should be %d/%d"% (pg,tot,i+1, pg_count),
                                     paging)
                    
            
        CheckStrategy.prepare_results(self)
                
    