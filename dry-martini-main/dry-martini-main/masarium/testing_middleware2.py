import dash
from werkzeug.wsgi import DispatcherMiddleware
import flask
from werkzeug.serving import run_simple
import dash_html_components as html
import gentabs
import genctb
# import login_f
import dash_core_components as dcc
from hrpgm.utilities import *
# from app import app as dash_app1
import os
from bs4 import BeautifulSoup
import requests
from flask import request as flask_request  
import hashlib
import numpy as np
from server import server
# from reports import dash_app2
# from register2 import dash_app3
from dash_app2 import dash_app2
from dash_app3 import dash_app3
# from header_app import app as dash_app4
from werkzeug.security import check_password_hash
from dash_app1 import dash_app1
from dash_app4 import dash_app4
from dash_app5 import dash_app5


# ############################################
# import os
from flask_login import logout_user, current_user, login_user, login_required, fresh_login_required, confirm_login
# from flask_login import LoginManager, UserMixin
# from users_mgt import db, User as base
# from config import config
# from flask import jsonify
from flask import g
# ############################################3
    
    
    




####################################################

app = DispatcherMiddleware(server, {
    '/dash1': dash_app1.server,
    '/dash2': dash_app2.server,
    '/dash3': dash_app3.server,
    '/dash4': dash_app4.server,
    '/dash5': dash_app5.server
})


# ####################################################


for view_func in server.view_functions:
#     print(view_func)
    if (view_func.startswith('/register') | view_func.startswith('/reports')| view_func.startswith('/bet')):
        server.view_functions[view_func] = login_required(server.view_functions[view_func])
# #################################################################

# with dash_app3.server.app_context():

#     print(">>>>",g.user)

@server.route('/')
def render_dashboard():
    return flask.redirect('/dash1')

@server.route('/hello')
def hello():
    return 'hello world!'

@server.route('/register')
@login_required
def reg():
#     print(">>>>>>>>>>>",current_user.get_id(),"<<<<<<<<<<<<<<<")
    return flask.redirect('/dash3')  

@server.route('/bet')
@login_required
def bett():
    return flask.redirect('/dash5')  

@server.route('/reports')
@login_required
def render_reports():
    return flask.redirect('/dash2')

@server.route('/login')
def login():
#     confirm_login()
    return flask.redirect('/dash4')  



server.title="ABCD"
if __name__ == '__main__':
    run_simple('0.0.0.0', 60288, app, use_reloader=True)
#     run_simple('0.0.0.0', 8050, app, use_reloader=True, use_debugger=True)
