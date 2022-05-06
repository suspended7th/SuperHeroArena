from flask import abort, Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_nav.elements import View
import json, requests, os, re

superHeroAPIURL = 'https://superhero-search.p.rapidapi.com/api/'
superHeroAPIHeaders = {
    'X-RapidAPI-Host': 'superhero-search.p.rapidapi.com',
    'X-RapidAPI-Key': os.getenv('X-RapidAPI-Key')
}

def call_superhero_api(data, suburl=''):
    print(data)
    response = requests.get(superHeroAPIURL + suburl, headers=superHeroAPIHeaders, params=data)
    print(response)
    super_hero_text = response.text
    if not re.match(r'^[\{\[]', super_hero_text):
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