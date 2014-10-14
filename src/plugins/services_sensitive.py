# coding=utf-8 
'''
Created on Sep 15, 2014

@author: ivan
'''

from forbidden_words import ForbiddenWords

phrases=["Best Efforts",
"Best Endeavors",
"Best Practices",
"Technology Transfer",
"Knowledge Transfer",
"Knowledge Sharing",
"Guarantee",
"Warrant",
"Partner",
"Partnership",
"Will meet your needs",
"Will meet your requirements",
"Will meet your expectations",
"Will exceed your needs",
"Will exceed your requirements",
"Will exceed your expectations",
"Satisfy",
"to customer.?s satisfaction",
"successfully",
"subject to customer.?s satisfaction",]

def create_instance():
    i= ForbiddenWords(phrases)
    i.change_name('Services Sensitive Phrases')
    i.set_optional(True)
    i.change_help("""<B>Sensitive Services Phrases</B><BR>
<BR>
This check applies to services ODs only.
<BR>
Identified phrases should not be in services ODs.
""")
    return i
