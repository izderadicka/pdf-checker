'''
Created on Jan 9, 2015

@author: ivan
'''



class Column(object):
    def __init__(self, header, left, right,  margin_bottom=None):
        self.pg_no=header.page_no
        if margin_bottom is None:
            margin_bottom=header.pg.height*0.05
        self._l=left
        self._r = right
        self._margin_bottom = margin_bottom
        self._closed=False
        self._bottom = header.bbox[3]
        self._data = []
        
        
    @property
    def closed(self):
        return self._closed
    
    def close(self):
        self._closed = True
        
    def try_add(self, line):
        if  (line.page_no != self.pg_no) or \
            (self._bottom - line.bbox[1]  > self._margin_bottom):
            self.close()
            return
        if (line.bbox[0]>=self._l) and (line.bbox[2]<= self._r):
            self._data.append(line.text)
            self._bottom = line.bbox[3]
            return True
            
    @property
    def data(self):
        return self._data
    
    @property
    def empty(self):
        return bool(self._data)
    
    @property
    def length(self):
        len(self._data)