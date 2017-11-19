"""Tests for learning journal app."""
from pyramid_scaffold.models import Entry, get_tm_session
from pyramid_scaffold.models.meta import Base
from pyramid.testing import DummyRequest
from datetime import datetime
from pyramid.httpexceptions import HTTPNotFound, HTTPFound, HTTPBadRequest
from pyramid import testing
import pytest
import transaction


def test_home_route_get_request_is_200_ok(testapp):
    """Test for status 200 ok."""
    response = testapp.get('/')
    assert response.status_code == 200


def test_home_route_get_no_entries_has_no_h2_tags(testapp):
    """Test there are no h2 tags when no entries available."""
    


def test_list_view_returns_a_list(dummy_request):
    """Will test that a list is returned."""
    from pyramid_scaffold.views.default import list_view
    response = list_view(dummy_request)
    assert isinstance(response['entries'], list)


def test_entry_exists_and_is_in_list(dummy_request):
    """Test that an entry is in the list."""
    from pyramid_scaffold.views.default import list_view
    new_entry = Entry(
        title='Test title',
        body='Test body.',
        creation_date=datetime.now()
    )
    dummy_request.dbsession.add(new_entry)
    dummy_request.dbsession.commit()
    response = list_view(dummy_request)
    assert new_entry.to_dict() in response['entries']


def test_detail_view_shows_entry_detail(dummy_request):
    """Test that the detail view displays the entry details."""
    from pyramid_scaffold.views.default import detail_view
    new_entry = Entry(
        title='Test title',
        body='Test body.',
        creation_date=datetime.now()
    )
    dummy_request.dbsession.add(new_entry)
    dummy_request.dbsession.commit()
    dummy_request.matchdict['id'] = 1
    response = detail_view(dummy_request)
    assert response['entry'] == new_entry.to_dict()


def test_detail_view_non_existent_entry(dummy_request, new_dict):
    """Test non existent entry raises HTTPNotFound error."""
    from pyramid_scaffold.views.default import detail_view
    dummy_request.matchdict['id'] = 2
    with pytest.raises(HTTPNotFound):
        detail_view(dummy_request)


def test_create_view_makes_new_entry(dummy_request):
    """Test new create view makes new entry."""
    from pyramid_scaffold.views.default import create_view
    entry_info = {
        "title": "New entry",
        "body": "This is the body"
    }
    dummy_request.method = "POST"
    dummy_request.POST = entry_info
    create_view(dummy_request)
    entry = dummy_request.dbsession.query(Entry).first()
    assert entry.title == "New entry"


def test_create_view_on_post_redirects_to_home_page(dummy_request):
    """Test new entry will redirect to the home page."""
    from pyramid_scaffold.views.default import create_view
    entry_info = {
        "title": "New entry",
        "body": "This is the body"
    }
    dummy_request.method = "POST"
    dummy_request.POST = entry_info
    response = create_view(dummy_request)
    assert isinstance(response, HTTPFound)


def test_create_view_incomplete_data_placeholder_text(dummy_request):
    """Test an incomplete POST will return a HTTPBadRequest."""
    from pyramid_scaffold.views.default import create_view
    entry_info = {
        "title": 'Test title',
    }
    dummy_request.method = "POST"
    dummy_request.POST = entry_info
    with pytest.raises(HTTPBadRequest):
        create_view(dummy_request)


def test_update_view_works(dummy_request, new_entry):
    """Test the update view returns a dict."""
    from pyramid_scaffold.views.default import update_view
    dummy_request.matchdict['id'] = 1
    response = update_view(dummy_request)
    assert isinstance(response, dict)


def test_update_view_updates_entry(dummy_request, new_entry):
    """."""
    from pyramid_scaffold.views.default import update_view
    new_info = {'title': 'New Title', 'body': 'New Body'}
    dummy_request.matchdict['id'] = 1
    dummy_request.method = "POST"
    dummy_request.POST = new_info
    update_view(dummy_request)
    entry = dummy_request.dbsession.query(Entry).get(1)
    assert entry.title == 'New Title'


@pytest.fixture(scope="session")
def testapp(request):
    """Test app for learning journal tests."""
    from webtest import TestApp
    from pyramid.config import Configurator

    def main():
        settings = {
            'sqlalchemy.url': 'postgres://localhost:5432/test_pyramid_scaffold'
        }
        config = Configurator(settings=settings)
        config.include('pyramid_jinja2')
        config.include('pyramid_scaffold.routes')
        config.include('pyramid_scaffold.models')
        config.scan()
        return config.make_wsgi_app()

    app = main()

    session_factory = app.registry["dbsession_factory"]
    engine = session_factory().bind
    Base.metadata.create_all(bind=engine)

    def tearDown():
        Base.metadata.drop_all(bind=engine)

    request.addfinalizer(tearDown)

    return TestApp(app)


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


def test_delete_has_deleted_data(testapp, fill_the_db):
    """Test that delete will delete a post."""
    response = testapp.get("/journal/3/delete")
    assert 'Test Journal 3' not in response


def test_create_view_successful_post_redirects_home(testapp):
    """Test that a new post will redirect to the list view (home page)."""
    entry_info = {
        "title": "Test title",
        "body": "Test body"
    }
    response = testapp.post("/create", entry_info)
    assert response.location == 'http://localhost/'
