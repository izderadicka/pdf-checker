PDF Checker
===========

PDF checker is a simple framework to create test/checks of PDF documents for certain text patterns, text organization etc.
For instance  it can check for "forbidden" words or  it can check that all numbered headings are in order or many other checks.

Check [project page](http://zderadicka.eu/projects/python/pdf-checker/) for details.

How it works
------------

PDF document is decomposend to individual text lines and these are supplied to checker. Checker can use some text tools (like regular expressions) to see if 
document is fine.   Checkers are plugins - so other checkers can be easily provided (see plugins directory - checker is subclass of CheckStrategy class).

A checker reports back errors together with their position in document (page ,% of page height and text bounding box coordinates). 

PDF Checker has command line interface (checker.py) or web based user interface (server.py) - which also displays PDF document and highlights errors on the document.

Install (on Debian Wheezy)
--------------------------
```
apt-get install build-essential python python-dev git python-pip uwsgi uwsgi-plugin-python nginx-full 
cd /opt
git clone https://github.com/izderadicka/pdf-checker.git checker
cd checker
pip  install -r requirements.pip
cp checker-uwsgi.ini /etc/uwsgi/apps-available/
ln -s /etc/uwsgi/apps-available/checker-uwsgi.ini /etc/uwsgi/apps-enabled
/etc/init.d/uwsgi restart
cp checker-nginx /etc/nginx/sites-available/
ln -s /etc/nginx/sites-available/checker-nginx  /etc/nginx/sites-enabled
/etc/init.d/nginx restart
```

License
-------

GPL ver.3 - check it here http://www.gnu.org/copyleft/gpl.html

Dependencies
------------
Python 2.7
pdfminer >= 20140328
Flask >= 0.10.1

History
-------

v0.1 - initial version - alpha quality

v0.2 - production version

v.0.2.1 - small fixes, some more checks
