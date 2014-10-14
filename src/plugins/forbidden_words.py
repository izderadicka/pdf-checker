# coding=utf-8 
'''
Created on Sep 1, 2014

@author: ivan
'''

import re
from common import CheckStrategy, Problem

class ForbiddenWords(CheckStrategy):
    name="Forbidden Words Check"
    
    def __init__(self, words):
        super(ForbiddenWords, self).__init__()
        res=[]
        terms=[]
        for w in words:
            r=re.compile(r'(\s|^)'+w+r'(\s|$)', re.IGNORECASE|re.UNICODE)
            terms.append(w)
            res.append(r)
        self._res=res
        self._words=terms
        
        
    def feed(self, line):
        for i,w in enumerate(self._res):
            for m in w.finditer(line.text):
                bbox=line.get_bbox(m.start(), m.end())
                p=Problem('Found forbidden phrase: %s'%self._words[i], line)
                p.bbox=bbox
                self.results.add_problem(p)
                
    
def create_instance():
    i= ForbiddenWords(['TBD', 'xx+', 'Dummy'])
    i.change_help("""<B>Forbidden Words Check</B><BR>
<BR>
We check the "forbidden" words, which should not be on the Ordering document.
<BR><BR>
Forbidden words are: <B>XX, XXX, TBD, Dummy</B><BR><BR>
""")
    return i
                