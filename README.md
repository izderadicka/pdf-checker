PDF Checker
===========

PDF checker is a simple framework to create test/checks of PDF documents for certain text patterns, text organization etc.
For instance  it can check for "forbidden" words or  it can check that all numbered headings are in order or many other checks.

How it works
------------

PDF document is decomposend to individual text lines and these are supplied to checker. Checker can use some text tools (like regular expressions) to see if 
document is fine.   Checkers are plugins - so other checkers can be easily provided (see plugins directory - checker is subclass of CheckStrategy class).

A checker reports back errors together with their position in document (page ,% of page height and text bounding box coordinates). 

PDF Checker has command line interface (checker.py) or web based user interface (server.py) - which also displays PDF document and highlights errors on the document.


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
