from flask import abort, Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_nav.elements import View
import json, requests, os, re, random

from .api import call_superhero_api

bp = Blueprint('battle', __name__, url_prefix='/battle')

@bp.route('/', methods=['POST'])
@login_required
def battle():
    data = {'hero': request.form['hero']}
    print(data)
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
    
    print(super_hero)
    print(enemy)
        
    return render_template('super_hero_battle.html', player=super_hero, enemy=enemy)
