#! /usr/bin/env python
'''
Created on Aug 15, 2014

@author: ivan
'''

from flask import Flask, render_template, request, url_for, send_from_directory, redirect
from werkzeug.exceptions import BadRequest  # @UnresolvedImport
import os.path
import tempfile
import subprocess
from checker import load_plugins
from _version import __version__
import urllib
import errno
import itertools
from flask.helpers import make_response
from flask_login import login_required
from access import register_with_app, current_user
import sys
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import json


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

db=None

if app.config.get('SQLALCHEMY_DATABASE_URI'):
    
    if app.config.get('SQLALCHEMY_DATABASE_URI').startswith("oracle"):
        os.environ['NLS_LANG']= 'AMERICAN_AMERICA.AL32UTF8'

    db = SQLAlchemy(app)
    class Check(db.Model):
        __tablename__ = 'pdf_check'
        id=db.Column(db.Integer, db.Sequence('pdf_check_pk_seq'), primary_key=True)
        username=db.Column(db.Unicode(200), nullable=False)
        filename=db.Column(db.Unicode(200), nullable=False)
        doc_type=db.Column(db.String(20), nullable=False)
        checked_on=db.Column(db.DateTime(timezone=True), nullable=False)
        
    class Issue(db.Model):
        __tablename__='pdf_issue'
        id=db.Column(db.Integer, db.Sequence('pdf_issue_pk_seq'), primary_key=True)
        check_type=db.Column(db.Unicode(200), nullable=False)
        error_msg=db.Column(db.Unicode(1000))
        page_no=db.Column(db.Integer)
        page_top=db.Column(db.Float)
        check_id=db.Column(db.Integer, db.ForeignKey('pdf_check.id'), nullable=False)
        check=db.relationship(Check)#, primaryjoin= check_id == Check.id)


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

def record_result(fname,cat,res):
    if current_user.is_authenticated():
        uname=current_user.id
    else:
        uname="anonymous"
        
    checks=json.loads(res)
    c=Check(username=uname, 
            filename=fname,
            doc_type=cat,
            checked_on = datetime.now()
            )
    db.session.add(c)
    for check in checks:
        for p in check['problems']:
            issue=Issue(check=c, 
                        check_type=check['check_name'],
                        error_msg=p['text'],
                        page_no=p['page'],
                        page_top=p['top'])
            db.session.add(issue)
    
    db.session.commit()

@app.route("/upload", methods=["GET","POST"])
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
            if db and not err:
                try:
                    record_result(f.filename, cat, res)
                except Exception,e:
                    app.logger.error('Error when recording results to db: %s',e)
                    import traceback;traceback.print_exc()
            return resp
        else:
            raise BadRequest('Not a PDF file!')
    else:
        return redirect(url_for('root'))
            
            
             
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
