"""."""
from pyramid.config import Configurator
from pyramid_scaffold.models.meta import Base
from pyramid_scaffold.models import Entry, get_tm_session
from pyramid import testing
import transaction
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
def configuration(request):
    """Set up an instance of the configurator."""
    config = testing.setUp(settings={
        'sqlalchemy.url': 'postgres://localhost:5432/test_pyramid_scaffold'
    })
    config.include("pyramid_scaffold.models")
    config.include("pyramid_scaffold.routes")

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture
def dummy_request(db_session):
    """Fake HTTP Request."""
    return testing.DummyRequest(dbsession=db_session)


@pytest.fixture
def db_session(configuration, request):
    """Create a database session."""
    session_factory = configuration.registry["dbsession_factory"]
    session = session_factory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def testapp(request):
    """Fixture for a fully configured test application."""
    from webtest import TestApp
    app = main({})

    SessionFactory = app.registry['dbsession_factory']
    engine = SessionFactory().bind
    Base.metadata.create_all(bind=engine)

    def tearDown():
        Base.metadata.drop_all(bind=engine)

    request.addfinalizer(tearDown)
    return TestApp(app)


@pytest.fixture
def one_db_entry(testapp):
    """Add one entry to the test db."""
    SessionFactory = testapp.app.registry["dbsession_factory"]
    session = SessionFactory()
    new_entry = Entry(
        title='Test Entry',
        body='Test Body'
    )
    session.add(new_entry)
    session.commit()


@pytest.fixture(scope="session")
def fill_the_db(testapp):
    """Fill the db for the testapp."""
    session_factory = testapp.app.registry["dbsession_factory"]
    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        dbsession.add_all(ENTRIES)

ENTRIES = []
for i in range(1, 20):
    new_entry = Entry(
        title='Test Journal {}'.format(i),
        body='Test body'
    )
    ENTRIES.append(new_entry)
