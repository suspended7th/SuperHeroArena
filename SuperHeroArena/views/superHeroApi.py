from flask import abort, Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_nav.elements import View
import json, requests, os, re

bp = Blueprint('shapi', __name__, url_prefix='/supers')

superHeroAPIURL = 'https://superhero-search.p.rapidapi.com/api/'
superHeroAPIHeaders = {
    'X-RapidAPI-Host': 'superhero-search.p.rapidapi.com',
    'X-RapidAPI-Key': os.getenv('X-RapidAPI-Key')
}

def call_superhero_api(data, suburl=''):
    response = requests.get(superHeroAPIURL + suburl, headers=superHeroAPIHeaders, params=data)
    super_hero_text = response.text
    if super_hero_text == 'Hero Not Found':
        return super_hero_text
    super_hero = json.loads(super_hero_text)
    if type(super_hero) is dict:
        super_hero = reformat_super_hero(super_hero)
    else:
        for i in range(0, len(super_hero)):
            super_hero[i] = reformat_super_hero(super_hero[i])
    return super_hero

def reformat_super_hero(super_hero):
    super_hero['biography']['alterEgos'] = re.split(r'[,;]\s', super_hero['biography']['alterEgos'])
    super_hero['work']['occupation'] = re.split(r'[,;]\s', super_hero['work']['occupation'])
    super_hero['work']['base'] = re.split(r';\s', super_hero['work']['base'])
    super_hero['connections']['groupAffiliation'] = re.split(r'[,;]\s', super_hero['connections']['groupAffiliation'])
    super_hero['connections']['relatives'] = re.split(r'(?<=\))[,;]\s', super_hero['connections']['relatives'])
    aliases = []
    for alias in super_hero['biography']['aliases']:
        aliases.extend(re.split(r'[,;]\s', alias))
    super_hero['biography']['aliases'] = aliases
    return super_hero

@bp.route('/', methods=['GET'])
def search():
    super_hero = {}
    if 'type' in request.args:
        type = request.args.get('type')
        data = {}
        error = ''
        if type == 'name':
            data = {'hero': request.args.get('hero')}
        elif type == 'regex':
            data = {'regex': request.args.get('regex')}
        elif type == 'simple_regex':
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
            if super_hero == 'Hero Not Found':
                flash(super_hero)
                super_hero = {}
            elif type == 'name':
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
