from flask_nav.elements import Navbar
from . import index, auth, superHeroApi

def generate_nav():
    index_nav = index.generate_nav()
    auth_nav = auth.generate_nav()
    superHeroApi_nav = superHeroApi.generate_nav()
    navs = [index_nav]
    if auth_nav:
        navs.append(auth_nav)
    if superHeroApi_nav:
        navs.append(superHeroApi_nav)
    return Navbar(*navs)