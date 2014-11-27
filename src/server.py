#! /usr/bin/env python
'''
Created on Aug 15, 2014

@author: ivan
'''

from flask import Flask, render_template, request, url_for, send_from_directory
from werkzeug.exceptions import BadRequest  # @UnresolvedImport
import os.path
import tempfile
import subprocess
from checker import load_plugins
from _version import __version__
from flask import json
import urllib
import errno
import itertools
from flask.helpers import make_response
from flask_login import login_required
from access import register_with_app
import sys


def get_checks():
    cl=[(p.name, p.categories if hasattr(p,'categories') else [], hasattr(p,'help') and p.help) for p in load_plugins()]
    #cl=[('A'+str(i), bool(i%2)) for i in xrange(13)]
    cl.sort(key=lambda x: x[0])
    cats = sorted(list(set(itertools.chain(*map(lambda c : c[1], cl)))))
    return cl, cats

app= Flask(__name__)
#app.debug = True
app.secret_key = os.urandom(24)
app.config['CHECKS'], app.config['CATEGORIES']=get_checks()
app.config.from_pyfile(os.path.join(os.path.dirname(__file__), '../site.cfg.py'))

register_with_app(app, 'root')

TMP_DIR='/tmp/pdf-checker-tmp'
if not os.path.exists(TMP_DIR):
    #FIX-BUG: can cause race condition if running few instances of same server
    try:
        os.mkdir(TMP_DIR)
    except OSError,e:
        if e.errno == errno.EEXIST:
            pass # ignore if exixtsOSError
        else:
            raise

@app.context_processor
def inject_version():
    return {'version':__version__}

@app.route("/")
@login_required
def root():
    return render_template('home.html', checks=app.config['CHECKS'], 
        cats2= [(c[0],c[1]) for c in app.config['CHECKS']],
        categories= app.config['CATEGORIES'],
        cat=request.cookies.get('category'))
def is_pdf(f):
    if not f: return False
    ext=os.path.splitext(f.filename)[1]
    return ext.lower() == '.pdf'

@app.route("/upload", methods=["POST"])
@login_required
def upload():
    if request.method == 'POST':  # @UndefinedVariable
        f = request.files['file']  # @UndefinedVariable
        if is_pdf(f):
            tfile=tempfile.NamedTemporaryFile(suffix=".pdf", delete=False, dir=TMP_DIR)
            f.save(tfile)
            tfile.close()
            checks=request.form.getlist('checks')
            cat=request.form.get('cat')
            res,err=run_checker( tfile.name, checks)
            tmp_file = os.path.split(tfile.name)[1]
            doc_url=url_for('files', filename=tmp_file)
            #os.remove(tfile.name)
            resp = make_response(render_template('result.html', 
                        result=res,
                        fname=f.filename,
                        doc_url=doc_url,
                        error=err))
            resp.set_cookie('category', cat, max_age=315360000)
            return resp
        else:
            raise BadRequest('Not a PDF file!')
    else:
        raise BadRequest('Only POST method allowed')
            
            
             
def run_checker(fname, checks=[]):
    pparams= ['python', 'checker.py', '--json',]
    for c in checks:
        pparams.append('-c')
        pparams.append(c)
    pparams.append(fname)
    print 'PROC:', ' '.join(pparams)
    p=subprocess.Popen(pparams, stdout=subprocess.PIPE, stderr= subprocess.PIPE)     
    result, err=p.communicate()
    
    return result, err

@app.route('/files/<filename>')
def files(filename):
    return send_from_directory(TMP_DIR,
                               filename)        
@app.route('/help/<check_name>')  
@login_required
def help_check(check_name):    
    for check in app.config['CHECKS']:
        if urllib.unquote(check_name) == check[0]:
            return json.jsonify(help=check[2])
    return json.jsonify(notFound=True, help=None)

if __name__ == "__main__":
    dbg=True
    if len(sys.argv)>1 and sys.argv[1]=='NO_DEBUG':
        dbg=False
        
    app.run(debug=dbg,)
