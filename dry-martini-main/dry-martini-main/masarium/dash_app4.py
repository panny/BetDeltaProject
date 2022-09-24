import flask

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input
from server import server, User
from flask_login import logout_user, current_user, login_user, login_required, fresh_login_required, confirm_login
from werkzeug.security import check_password_hash
import os
import pickle

dash_app4 = dash.Dash(__name__, server = server, url_base_pathname='/login/')


# _app_route = '/dash-core-components/logout_button'
_app_route = '/login'


# Create a login route
@dash_app4.server.route('/custom-auth/login', methods=['POST'])
def route_login():
    data = flask.request.form
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user:
        if check_password_hash(user.password, password):
            login_user(user)
        else:
            return 'Wrong username / password'
    else:
        return 'Wrong username / password' 
#     html.Div(dcc.Location(pathname="/login", id="locate"))

#     if not username or not password:
#         flask.abort(401)

    # actual implementation should verify the password.
    # Recommended to only keep a hash in database and use something like
    # bcrypt to encrypt the password and check the hashed results.

    # Return a redirect with
    print(flask.session['_id'])
    rep = flask.redirect(_app_route)

    # Here we just store the given username in a cookie.
    # Actual session cookies should be signed or use a JWT token.
    rep.set_cookie('custom-auth-session', username)
    return rep


# create a logout route
@dash_app4.server.route('/custom-auth/logout', methods=['POST'])
def route_logout():
    # Redirect back to the index and remove the session cookie.
    rep = flask.redirect(_app_route)
    rep.set_cookie('custom-auth-session', '', expires=0)
    logout_user()
    return rep


# Simple dash component login form.
login_form = html.Div(
              className='header',
            style={'height': '50'},
            children=[
                html.Img(
                    src='assets/logo.png',
                    className='logo', style={'display':'inline-block'}
                ),
    html.Form([
        dcc.Input(placeholder='username', name='username', type='text'),
        dcc.Input(placeholder='password', name='password', type='password'),
        html.Button('Login', type='submit')
    ], style={'display':'inline-block'}, action='/custom-auth/login', method='post')
])

session_cookie=''
actno=''
bal=''
logout_form = html.Div(
              className='header',
            style={'height': '50'},
            children=[
                html.Img(
                    src='assets/logo.png',
                    className='logo', style={'display':'inline-block'}
                ),
                html.Div(f'Hello {session_cookie} account no {actno} with last login balance: {bal}', style={'display':'inline-block'}),
                dcc.LogoutButton(logout_url='/custom-auth/logout', style={'display':'inline-block'})
                
])


dash_app4.layout = html.Div(id='custom-auth-frame')


@dash_app4.callback(Output('custom-auth-frame', 'children'),
              [Input('custom-auth-frame', 'id')])
def dynamic_layout(_):
    session_cookie = flask.request.cookies.get('custom-auth-session')

    if not session_cookie:
        # If there's no cookie we need to login.
        return login_form
    
    ba_pth = 'hrpgm/betaccounts/'
    ba_ip= "xx"+flask.request.environ.get('HTTP_X_REAL_IP', flask.request.remote_addr)
#     bal=''
#     actno=''
    if os.path.isfile(ba_pth+f'{ba_ip}.pickle') :
        with open(ba_pth+f'{ba_ip}.pickle', 'rb') as infile:
            account=pickle.load(infile)
        bal = account['getin']['balance']
        actno = account['getin']['betaccount']
    return logout_form


if __name__ == '__main__':
    dash_app4.run_server(host="0.0.0.0", port=8050, debug=True)
