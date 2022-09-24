from flask import Flask, render_template

server = Flask(__name__)

############################################
import os
from flask_login import logout_user, current_user, login_user, login_required, fresh_login_required
from flask_login import LoginManager, UserMixin, AnonymousUserMixin
from users_mgt import db, User as base
from config import config
from flask import jsonify

############################################3

####################################################



# config
server.config.update(
    SECRET_KEY=os.urandom(12),
    SQLALCHEMY_DATABASE_URI=config.get('database', 'con'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db.init_app(server)

# Setup the LoginManager for the server
login_manager = LoginManager()
login_manager.init_app(server)
# login_manager.init_app(dash_app1.server)
# login_manager.init_app(dash_app2.server)
# login_manager.init_app(dash_app3.server)
# login_manager.init_app(dash_app4.server)

login_manager.login_view = '/login'
login_manager.refresh_view = "/reauth"


# Create User class with UserMixin
class User(UserMixin, base):
    pass

class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.username = 'Guest'

# callback to reload the user object
@login_manager.user_loader
def load_user(user_id):  
    return User.query.get(int(user_id))




# @login_manager.unauthorized_handler
# def unauth_handler():
#     return jsonify(success=False,
#                    data={'login_required': True},
#                    message=f'Authorize please to access this page'), 401

