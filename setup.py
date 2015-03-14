try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'GrantsBot, a bot for updating and maintaining the IdeaLab',
    'author': 'Jonathan Morgan and Frances Hocutt',
    'url': 'https://github.com/jtmorgan/grantsbot',
    'download_url': '',
    'author_email': 'jmorgan@wikimedia.org',
    'version': '',
    'install_requires': ['nose'],
    'packages': ['grantsbot', 'matching'],
    'scripts': ['scoreboard.py'],
    'name': 'GrantsBot'
}

setup(**config)
