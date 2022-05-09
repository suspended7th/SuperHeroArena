from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_required
import math, random

from .api import call_superhero_api

bp = Blueprint('battle', __name__, url_prefix='/battle')

@bp.route('/', methods=['POST'])
@login_required
def battle():
    data = {'hero': request.form['hero']}
    super_hero = call_superhero_api(data)
    if type(super_hero) != dict and type(super_hero) != list:
        flash(super_hero)
        return redirect('/supers/')
    enemy = {}
    if super_hero['biography']['alignment'] == 'good':
        enemy = call_superhero_api({}, 'villains')
    else:
        enemy = call_superhero_api({}, 'heroes')
    
    enemy = random.choice(enemy)
    
    hp = request.form['hp']
    score = int(request.form['score'])
    hp_percent = str(math.ceil(int(hp) / 300 * 100))
        
    return render_template('super_hero_battle.html', player=super_hero, enemy=enemy, hp=hp, score=score, hp_percent=hp_percent)
