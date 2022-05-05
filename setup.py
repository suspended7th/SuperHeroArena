from setuptools import setup

setup(
    name='SuperHeroArena',
    packages=['SuperHeroArena'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask_sqlalchemy',
        'passlib',
        'flask_login',
        'requests',
        'python-dotenv'
    ],
)