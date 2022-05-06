from flask import abort, Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_nav.elements import View
import json, requests, os, re

from .api import call_superhero_api

bp = Blueprint('shapi', __name__, url_prefix='/supers')

@bp.route('/', methods=['GET'])
@login_required
def search():
    super_hero = {}
    if 'type' in request.args:
        request_type = request.args.get('type')
        data = {}
        error = ''
        if request_type == 'name':
            data = {'hero': request.args.get('hero')}
        elif request_type == 'regex':
            data = {'regex': request.args.get('regex')}
        elif request_type == 'simple_regex':
            regex = '.*'
            name = request.args.get('simple_regex')
            for letter in name:
                regex += '[{}{}]'.format(letter.upper(), letter.lower())
            regex += '.*'
            data = {'regex': regex}
        else:
            error = 'There was an error in parsing which type of query you are trying to make.'
            flash(error)
        if not error:
            super_hero = call_superhero_api(data)
            if type(super_hero) is str:
                flash(super_hero)
                super_hero = {}
            elif request_type == 'name':
                super_hero = [super_hero]
    else:
        if 'heroes' in request.args:
            super_hero = call_superhero_api({}, 'heroes')
        elif 'villains' in request.args:
            super_hero = call_superhero_api({}, 'villains')
    return render_template('super_hero_lookup.html', supers=super_hero)

def generate_nav():
    if current_user.is_authenticated:
        return View('Super Hero Search', 'shapi.search')
    return None
