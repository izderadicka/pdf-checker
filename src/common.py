'''
Created on Aug 17, 2014

@author: ivan
'''
import StringIO
import json

class CheckStrategy(object):
    def __init__(self):
        self.results=Result(self.name)
    name=""
    def feed(self, txt):
        raise NotImplemented()
    def get_results(self):
        return self.results
    def change_name(self, new_name):
        self.name=new_name
        self.results.for_check=new_name
class Problem(object):
    def __init__(self, descr, on):
            self.text=descr
            self.page=on.page_no
            self.top=on.top
            self.bbox=on.bbox
        
class Result(object):
    def __init__(self, for_check):
        self.for_check=for_check
        self.problems=[]
        
    def add(self, descr, on):
        self.problems.append(Problem(descr,on))
        
    def add_problem(self, p):
        self.problems.append(p)
        
        
    @property
    def failure(self):
        return len(self.problems)>0
    
    def __unicode__(self):
        buff=StringIO.StringIO()
        buff.write(u'CHECK: %s result: %s\n' %(self.for_check, 'FAILED' if self.failure else "OK"))
        if self.failure:
            buff.write(u'-'*60)
            buff.write('\n')
            buff.writelines(map(lambda p: u"(pg.{0.page:d} at {0.top:0.0f}%) {0.text}\n".format(p),
                                   self.problems))
            buff.write(u'-'*60)
            buff.write('\n')
        return buff.getvalue()
    
    def to_json(self):
        return json.dumps ({ 'check_name':self.for_check,
                'problems':[{'page':p.page, 'top':p.top, 'bbox':p.bbox, 'text':p.text} for p in self.problems]
            })
            
        
        
        
    def __str__(self):
        return u"(pg=%d, left=%f%%, top=%f%%) %s " % (self.page_no, self.left, self.top, self.text)
    
    def __repr__(self):
        return self.__str__()