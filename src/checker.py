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
from pdfminer.layout import LAParams, LTTextBox
import sys
import plugins
import os,os.path
import importlib
from inspect import isclass
from common import CheckStrategy

def load_plugins(filter):
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
    def __init__(self, text, page_no, left, top, bbox):
        self.text=text
        self.page_no=int(page_no)
        self.left=left
        self.top=top
        self.bbox=bbox
        
    def __unicode__(self):
        return u"[pg:{0.page_no}, top:{0.top:0.0f}%, left:{0.left:0.0f}%, bbox:{0.bbox}] {0.text}".format(self)
        
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
                texts= filter(lambda t:t.text.strip(), map(lambda obj: TextLine(obj.get_text().strip(), page.pageid, 
                    _to_pct(obj.x0, page.width), _to_pct(page.height-obj.y0, page.height), obj.bbox), line))
                for t in texts:
                    for s in strategies:
                        s.feed(t)
        
def main():
    parser = argparse.ArgumentParser('Check PDF file')
    parser.add_argument("document", help="PDF document to be analyzed")
    parser.add_argument("--debug", "-d", action="store_true", help="Print debug output of document ")
    parser.add_argument("--json", "-j", action="store_true", help="Output JSON ")
    parser.add_argument("--check", "-c",nargs="*", help="Checks to perform, can appear several times")
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
if __name__ == '__main__':
    main()