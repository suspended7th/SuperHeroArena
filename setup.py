from setuptools import setup

setup(
    name='SuperHeroArena',
    packages=['SuperHeroArena'],
    include_package_data=True,
    install_requires=[
        'wheel',
        'flask',
        'flask_sqlalchemy',
        'flask_bootstrap',
        'flask_nav',
        'passlib',
        'flask_login',
        'requests',
        'python-dotenv'
    ],
)