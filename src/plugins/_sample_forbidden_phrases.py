# coding=utf-8 
'''
Created on Sep 1, 2014

@author: ivan
'''

import re
from common import CheckStrategy, Problem

class ForbiddenWords(CheckStrategy):
    name="Sample Forbidden Words Check"
    
    
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
                p=Problem('Found problematic phrase: %s'%self._words[i], line)
                p.bbox=bbox
                self.results.add_problem(p)
                
# Only if check instance needs initialization, othewize can load plugin and init with no arguments
# Also useful when customizing other plugin to bit different check (use ForbiddenWords to check for other phrases     
def create_instance():
    i= ForbiddenWords(['TBD', 'xx+', 'Dummy'])
    i.set_categories(['Cat1', 'Cat2', 'Cat3'])
    i.change_help("""<B>Forbidden Words Check</B><BR>
<BR>
We check the "forbidden" words, which should not be on the document.
""")
    return i
                