'''
Created on Sep 15, 2014

@author: ivan
'''

from forbidden_words import ForbiddenWords

def create_instance():
    i= ForbiddenWords(['This Ordering Document must be executed by you and Oracle on or before'])
    i.change_name('Quote Validity Language Check')
    i.set_categories(['License'])
    i.change_help("""<B>Quote Validity Language Check</B><BR>
<BR>

We check the old validity phrase, which should not be on the Ordering document.<BR><BR>


Old validity phrase: <B>"This Ordering Document must be executed by you and Oracle on or before"</B><BR>
<BR>
This is the BAD / INCORRECT quote validity language and can result in a Rev-Rec issue. This language must be removed from the OD.
""")
    return i
