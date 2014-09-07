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

def get_checks():
    cl=[(p.name, hasattr(p,'optional') and p.optional) for p in load_plugins()]
    #cl=[('A'+str(i), bool(i%2)) for i in xrange(13)]
    cl.sort(key=lambda x: x[0])
    return cl
        

app= Flask(__name__)
#app.debug = True
app.secret_key = os.urandom(24)
app.config['CHECKS']=get_checks()

#app.permanent_session_lifetime = timedelta(seconds=60)

TMP_DIR='/tmp/pdf-checker-tmp'
if not os.path.exists(TMP_DIR):
    os.mkdir(TMP_DIR)

@app.context_processor
def inject_version():
    return {'version':__version__}


@app.route("/")
def root():
    return render_template('home.html', checks=app.config['CHECKS'])
def is_pdf(f):
    if not f: return False
    ext=os.path.splitext(f.filename)[1]
    return ext.lower() == '.pdf'

@app.route("/upload", methods=["POST"])
def upload():
    if request.method == 'POST':  # @UndefinedVariable
        f = request.files['file']  # @UndefinedVariable
        if is_pdf(f):
            tfile=tempfile.NamedTemporaryFile(suffix=".pdf", delete=False, dir=TMP_DIR)
            f.save(tfile)
            tfile.close()
            checks=request.form.getlist('checks')
            res,err=run_checker( tfile.name, checks)
            tmp_file = os.path.split(tfile.name)[1]
            doc_url=url_for('files', filename=tmp_file)
            #os.remove(tfile.name)
            return render_template('result.html', 
                        result=res,
                        fname=f.filename,
                        doc_url=doc_url,
                        error=err)
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
          

if __name__ == "__main__":
    app.run(debug=True,)
