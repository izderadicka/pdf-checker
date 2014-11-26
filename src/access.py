'''
Created on Nov 25, 2014

@author: ivan
'''
import sys
from flask import Blueprint, render_template, request, redirect, flash, url_for, make_response
from flask_login import LoginManager,login_user, logout_user, login_required
from flask_login import UserMixin

MAIN_VIEW=None

login_manager=LoginManager()
access=Blueprint('access', 'access')



def register_with_app(app, main_view="root"):
    global MAIN_VIEW
    MAIN_VIEW=main_view
    #app.permanent_session_lifetime = timedelta(seconds=60)
    app.register_blueprint(access, url_prefix="/access")
    login_manager.init_app(app)
    

class User(UserMixin):
    def __init__(self, id):
        self.id=id
        
        
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

def valid_login(uid, pwd):
    return len(uid)>=5

login_manager.login_view = "access.login"
@access.route('/login', methods=['GET', 'POST'])
def login():
    username=""
    if request.method=='POST':
        username=request.form['username']
        if valid_login(username,
                       request.form['password']):
            login_user(User(username))
            return redirect(request.args.get("next") or url_for(MAIN_VIEW))
        else:
            flash('Invalid user name or password!')
        
    return render_template('access/login.html', username=username)

@access.route('/logoff')
@login_required
def logoff():
    logout_user()
    return redirect(url_for(MAIN_VIEW))
        

        