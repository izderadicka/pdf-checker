#! /usr/bin/env python
'''
Created on Aug 5, 2014

@author: ivan
'''

import argparse
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox,LTChar
import sys
import plugins
import os,os.path
import importlib
from inspect import isclass
from common import CheckStrategy
import time

def load_plugins(filter=None):
    plugs=[]
    path=os.path.split(plugins.__file__)[0]
    for fname in os.listdir(path):
        mod,ext=os.path.splitext(fname)
        fname=os.path.join(path,fname)
        if os.path.isfile(fname) and ext=='.py' and not mod.startswith('_'):
            m=importlib.import_module('plugins.'+mod)
            plug=None
            if hasattr(m, 'create_instance'):
                plug=m.create_instance()
            else:
                for c in dir(m):
                    cls=getattr(m, c);
                    if not c.startswith('_') and isclass(cls) and issubclass(cls, CheckStrategy) \
                        and CheckStrategy != cls:
                        plug = cls()
            if plug and hasattr(plug, 'name'):
                if filter:
                    if plug.name in filter:
                        plugs.append(plug)
                else:
                    plugs.append(plug)
                    
    return plugs            
                

def _to_pct(val, max):
    return float(val)/max*100.0

class PrintBoxes():   
    name="Just Printing"
    def __init__(self):
        self.lines=[]
    def feed(self, txt):
        self.lines.append(txt)
        
    def get_results(self):
        return u'\n'.join(map(lambda l: unicode(l), self.lines))+u'\n\n'
        

class TextLine(object):
    def __init__(self, text, page_no, left, top, bbox, height, width, chars):
        self.text=text
        self.page_no=int(page_no)
        self.left=left
        self.top=top
        self.bbox=bbox
        self.height=height
        self.width=width
        assert len(text) <= len(chars)
        self.chars=chars
        
    @property
    def font_size(self):
        for i in xrange(len(self.chars)):
            if isinstance(self.chars[i], LTChar):
                return self.size_at(0)    
    
    def font_at(self, idx):
        return self.chars[idx].fontname
    
    def size_at(self, idx):
        return self.chars[idx].size
    
    class Bbox(object):
        pass
    
    def get_bbox(self, start, end):
        c1 = self.chars[start]
        while not hasattr(c1, 'x0') and not hasattr(c1, 'y0'):
            start-=1
            c1=TextLine.Bbox()
           
            if start<0:
                c1.x0=self.bbox[0]
                c1.y0=self.bbob[1]
            elif isinstance(self.chars[start], LTChar):
                c=self.chars[start]
                c1.x0=c.x1
                c1.y0=c.y0
            
        
        c2 = self.chars[end-1]
        while not hasattr(c2, 'x1') and not hasattr(c2, 'y1'):
            end+=1
            c2=TextLine.Bbox()
            if end >= len(self.chars):
                c2.x1=self.bbox[2]
                c2.y1=self.bbox[3]
            elif isinstance(self.chars[end-1], LTChar):
                c=self.chars[end-1]
                c2.x1=c.x0
                c2.y1=c.y1
        
        return (c1.x0, c1.y0, c2.x1, c2.y1)
        
        
    def __unicode__(self):
        return u"[pg:{0.page_no}, top:{0.top:0.0f}%, left:{0.left:0.0f}%, height:{0.height}, font-size:{0.font_size}] {0.text}".format(self)
        
    def __str__(self):
        return self.__unicode__()
        

        
class PdfMinerWrapper(object):
    """
    Usage:
    with PdfMinerWrapper('2009t.pdf') as doc:
        for page in doc.get_pages():
    """
    def __init__(self, pdf_doc, pdf_pwd=""):
        self.pdf_doc = pdf_doc
        self.pdf_pwd = pdf_pwd
    def __enter__(self):
        #open the pdf file
        self.fp = open(self.pdf_doc, 'rb')
        # create a parser object associated with the file object
        parser = PDFParser(self.fp)
        # create a PDFDocument object that stores the document structure
        doc = PDFDocument(parser, password=self.pdf_pwd)
        # connect the parser and document objects
        parser.set_document(doc)
        self.doc=doc
        return self
    
    def _parse_pages(self):
        rsrcmgr = PDFResourceManager()
        laparams = LAParams(char_margin=2.5)
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
    
        for page in PDFPage.create_pages(self.doc):
            interpreter.process_page(page)
            # receive the LTPage object for this page
            layout = device.get_result()
            # layout is an LTPage object which may contain child objects like LTTextBox, LTFigure, LTImage, etc.
            yield layout
    def __iter__(self): 
        return iter(self._parse_pages())
    
    def __exit__(self, _type, value, traceback):
        self.fp.close()
           
def process_doc(doc_name, strategies):
    def compareBoxes(o1,o2):
        if o1.y0>o2.y0:
            return -1
        elif o1.y0<o2.y0:
            return 1
        elif o1.x0<o2.x0:
            return -1
        elif o1.x0>o2.x0:
            return 1
        else:
            return 0
    with PdfMinerWrapper(doc_name) as doc:
        for page in doc:
            
            tbs= filter(lambda obj:isinstance(obj, LTTextBox), page)
            tbs.sort(cmp=compareBoxes)
            for line in tbs:
                texts= filter(lambda t:t.text, map(lambda obj: TextLine(obj.get_text().strip(), page.pageid, 
                    _to_pct(obj.x0, page.width), _to_pct(page.height-obj.y0, page.height), 
                    obj.bbox, obj.height, obj.width, filter(lambda c: c.get_text(),obj))
                    , line))
                for t in texts:
                    for s in strategies:
                        s.feed(t)
        
def main():
    start=time.time()
    parser = argparse.ArgumentParser('Check PDF file')
    parser.add_argument("document", help="PDF document to be analyzed")
    parser.add_argument("--debug", "-d", action="store_true", help="Print debug output of document ")
    parser.add_argument("--json", "-j", action="store_true", help="Output JSON ")
    parser.add_argument("--check", "-c",action="append", help="Checks to perform, can appear several times")
    args=parser.parse_args()
    strategies=[]
    if args.debug and not args.json:
        strategies.append(PrintBoxes())
    strategies.extend(load_plugins(args.check))
    process_doc(args.document, strategies)
    if args.json:
        sys.stdout.write('[')
        for i,s in enumerate(strategies):
            sys.stdout.write(s.get_results().to_json())
            if i< len(strategies)-1:
                sys.stdout.write(',')
        sys.stdout.write(']')
    else:
        for s in strategies:
            res= s.get_results()
            sys.stdout.write(unicode(res).encode('utf8'))
    if args.debug:
        print 'Finished in %f secs' % (time.time()-start)
if __name__ == '__main__':
    main()