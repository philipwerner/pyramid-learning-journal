"""."""
from pyramid.config import Configurator
import os


def main(global_config, **settings):
    """Function returns a Pyramid WSGI application."""
    if os.environ.get('DATABASE_URL', ''):
        settings['sqlalchemy.url'] = os.environ['DATABASE_URL']
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.add_static_view(name='static', path='pyramid_scaffold:static')
    config.include('.security')
    config.scan()
    return config.make_wsgi_app()
