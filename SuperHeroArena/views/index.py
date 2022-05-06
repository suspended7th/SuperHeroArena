from flask import render_template, Blueprint
from flask_nav.elements import View

bp = Blueprint('index', __name__)

@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

def generate_nav():
    return View('Home Page', 'index.index')
