"""."""
from pyramid.config import Configurator
from pyramid_scaffold.models.meta import Base
from webtest import TestApp
import pytest
import os


@pytest.fixture
def main(global_config, **settings):
    """Function returns a Pyramid WSGI application."""
    if os.environ.get('DATABASE_URL', ''):
        settings['sqlalchemy.url'] = os.environ['TEST_DB']
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('pyramid_scaffold.models')
    config.include('pyramid_scaffold.routes')
    config.add_static_view(name='static', path='pyramid_scaffold:static')
    config.include('pyramid_scaffold.security')
    config.scan()
    return config.make_wsgi_app()


@pytest.fixture
def testapp(request):
    """Fixture for a fully configured test application."""
    app = main({})

    SessionFactory = app.registry['dbsession_factory']
    engine = SessionFactory().bind
    Base.metadata.create_all(bind=engine)

    def tearDown():
        Base.metadata.drop_all(bind=engine)

    request.addfinalizer(tearDown)
    return TestApp(app)
