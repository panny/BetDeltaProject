from flask import Blueprint, render_template

api = Blueprint('api', __name__, template_folder='templates')

@api.route('/')
def home():
    return render_template('page/home.html')


@api.route('/terms')
def terms():
    return render_template('page/terms.html')


@api.route('/privacy')
def privacy():
    return render_template('page/privacy.html')