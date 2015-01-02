'''
Created on Nov 25, 2014

@author: ivan
'''
import os
from flask import Blueprint, render_template, request, redirect, flash, url_for, make_response, session
from flask_login import LoginManager,login_user, logout_user, login_required
from flask_login import UserMixin, current_user
from urlparse import urlparse
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.utils import OneLogin_Saml2_Utils



AUTH_PWD_FORM="PWD_FORM"
AUTH_SAML="SAML"

AUTHENTICATION_TYPE=AUTH_PWD_FORM

SAML_UID_ATTRIBUTE = None
BASE_SAML_PATH = os.path.dirname(os.path.dirname(__file__))

SAML_CONFIG={}

MAIN_VIEW=None

login_manager=LoginManager()
access=Blueprint('access', 'access')

#SAML_PATH = os.path.join(os.path.dirname(__file__), '../saml')

def register_with_app(app, main_view="root"):
    def set_globals(app, names):
        g=globals()
        for n in names:
            try:
                g[n]=app.config[n]
            except KeyError:
                raise Exception("Missing key %s in config file"%n)
    global MAIN_VIEW
    MAIN_VIEW=main_view
    set_globals(app, ['AUTHENTICATION_TYPE', 'SAML_UID_ATTRIBUTE', 'BASE_SAML_PATH'])
    SAML_CONFIG.update(app.config['SAML_ADVANCED_CONFIG'])
    SAML_CONFIG['sp'] = app.config['SAML_META_SP']
    SAML_CONFIG['idp'] = app.config['SAML_META_IDP']
    #app.permanent_session_lifetime = timedelta(seconds=60)
    app.register_blueprint(access, url_prefix="/access")
    login_manager.init_app(app)
    if AUTHENTICATION_TYPE == AUTH_SAML:
        login_manager.unauthorized_callback = saml_login
        login_manager.needs_refresh_callback = saml_login
        
   
    

class User(UserMixin):
    def __init__(self, id):
        self.id=id
        
        
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

def valid_login(uid, pwd):
    return len(uid)>=5

def init_saml_auth(req):
    auth = OneLogin_Saml2_Auth(req, SAML_CONFIG,custom_base_path=BASE_SAML_PATH)
    return auth


def prepare_flask_request(request):
    url_data = urlparse(request.url)
    return {
        'http_host': request.host,
        'server_port': url_data.port,
        'script_name': request.path,
        'get_data': request.args.copy(),
        'post_data': request.form.copy()
    }

def saml_login():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    return redirect(auth.login())

login_manager.login_view = "access.login"
@access.route('/login', methods=['GET', 'POST'])
def login():
    if AUTHENTICATION_TYPE==AUTH_PWD_FORM:
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
    elif AUTHENTICATION_TYPE == AUTH_SAML:
        if current_user.is_authenticated():
            return redirect(request.args.get("next") or url_for(MAIN_VIEW))
        else:
            return saml_login
    else:
        return ('Internal error', 500)
        
        

@access.route('/logoff')
@login_required
def logoff():
    if AUTHENTICATION_TYPE==AUTH_PWD_FORM:
        logout_user()
        return redirect(url_for(MAIN_VIEW))
    elif AUTHENTICATION_TYPE == AUTH_SAML:
        req = prepare_flask_request(request)
        auth = init_saml_auth(req)
        session_index = session.get('SAML_SESSION_INDEX')
        return redirect(auth.logout(name_id=current_user.get_id(), session_index=session_index))
    else:
        return ('Internal error', 500)
    

@access.route('/saml/metadata/')
def metadata():
    if AUTHENTICATION_TYPE == AUTH_SAML:
        req = prepare_flask_request(request)
        auth = init_saml_auth(req)
        settings = auth.get_settings()
        metadata = settings.get_sp_metadata()
        errors = settings.validate_metadata(metadata)
    
        if len(errors) == 0:
            resp = make_response(metadata, 200)
            resp.headers['Content-Type'] = 'text/xml'
        else:
            resp = make_response(errors.join(', '), 500)
        return resp
    else:
        return ('Not Found', 404)


def get_uid(attrs):
    pass

@access.route('/saml/sso/<action>', methods=['GET', 'POST'])
def sso(action):
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    errors = []

    if action=='acs':
        auth.process_response()
        errors = auth.get_errors()
        if not auth.is_authenticated():
            errors.append('user not authenticated')
        if SAML_UID_ATTRIBUTE:
            uid=auth.get_attribute(SAML_UID_ATTRIBUTE)
            if not uid:
                errors.append('uid attribute not found in response')
            elif len(uid)>1:
                errors.append('uid attribute has multiple values')
            else:
                uid=uid[0]
        else:
            uid=auth.get_nameid()
            if not uid:
                errors.append('nameID is not available')
        session_index = auth.get_session_index()
        if not session_index:
            errors.append('session index is not provided')
        else:
            session['SAML_SESSION_INDEX']=session_index
        if len(errors) == 0:
            login_user(User(uid))
            self_url = OneLogin_Saml2_Utils.get_self_url(req)
            if 'RelayState' in request.form and self_url != request.form['RelayState']:
                return redirect(auth.redirect_to(request.form['RelayState']))
            else: 
                return redirect(url_for(MAIN_VIEW))
    elif action=='sls':
        def dscb ():
            try:
                session.pop('SAML_SESSION_INDEX')
            except KeyError:
                pass
            logout_user()
        url = auth.process_slo(delete_session_cb=dscb)
        errors = auth.get_errors()
        if len(errors) == 0:
            if url is not None:
                return redirect(url)
            else:
                return redirect(url_for(MAIN_VIEW))
    else:
        return ('Invalid request', 400)

    for e in errors:
        flash(e)
    return render_template(
        'access/sso.html',
        
    )

        

        