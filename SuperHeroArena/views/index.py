from flask import render_template, Blueprint
from flask_nav.elements import View

from ..models.user import User

bp = Blueprint('index', __name__)

@bp.route('/', methods=['GET'])
def index():
    leaderboard = User.query.order_by(User.high_score.desc(), User.high_score_date).limit(10)
    return render_template('index.html', leaderboard=leaderboard)

def generate_nav():
    return View('Home Page', 'index.index')
