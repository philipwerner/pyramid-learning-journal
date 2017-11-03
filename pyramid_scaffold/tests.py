"""Tests for learning journal app."""
from pyramid_scaffold.data.data import ENTRIES
from pyramid.testing import DummyRequest
from pyramid import testing
from pyramid.response import Response
import pytest


def test_list_view_returns_dict():
    """Will test that a dict is returned from the list view."""
    from pyramid_scaffold.views.default import list_view
    req = testing.DummyRequest()
    response = list_view(req)
    assert isinstance(response, dict)


def test_list_view_returns_proper_amount_of_content():
    """Tests for proper content on homepage."""
    from pyramid_scaffold.views.default import list_view
    req = testing.DummyRequest()
    response = list_view(req)
    assert len(response['new_entries']) == len(ENTRIES)


def test_detail_view():
    """Test that the view returns a dictionary of values."""
    from pyramid_scaffold.views.default import detail_view
    req = testing.DummyRequest()
    req.matchdict['id'] = 5
    info = detail_view(req)
    assert isinstance(info, dict)


def test_detail_view_response_contains_entry_attr():
    """Test that the view returns one entry."""
    from pyramid_scaffold.views.default import detail_view
    req = testing.DummyRequest()
    req.matchdict['id'] = 5
    info = detail_view(req)
    for key in ["id", "title", "body", "creation_date"]:
        assert key in info["entry"]


def test_detail_page_http_not_found():
    """Test that a HTTPNotFound is raised."""
    from pyramid.httpexceptions import HTTPNotFound
    from pyramid_scaffold.views.default import detail_view
    req = testing.DummyRequest()
    req.matchdict['id'] = 100
    with pytest.raises(HTTPNotFound):
        detail_view(req)


def test_update_view():
    """Test that the view returns a dictionary of values."""
    from pyramid_scaffold.views.default import update_view
    req = testing.DummyRequest()
    req.matchdict['id'] = 5
    info = update_view(req)
    assert isinstance(info, dict)


def test_update_view_response_contains_entry_attr():
    """Test that the view returns one entry."""
    from pyramid_scaffold.views.default import update_view
    req = testing.DummyRequest()
    req.matchdict['id'] = 5
    info = update_view(req)
    for key in ["id", "title", "body", "creation_date"]:
        assert key in info["entry"]


@pytest.fixture()
def testapp():
    """Create and instance of our app for testing."""
    from webtest import TestApp
    from pyramid.config import Configurator

    def main():
        config = Configurator()
        config.include('pyramid_jinja2')
        config.include('.routes')
        config.scan()
        return config.make_wsgi_app()

    app = main()
    return TestApp(app)


def test_layout_root(testapp):
    """Test that the contents of the root page contains <article>."""
    response = testapp.get('/', status=200)
    html = response.html
    assert 'Philip Werner 2017' in html.find("footer").text


def test_root_contents(testapp):
    """Test that the contents of the root page contains as many <h3> tags as entries."""
    from pyramid_scaffold.data.data import ENTRIES
    response = testapp.get('/', status=200)
    html = response.html
    assert len(ENTRIES) == len(html.findAll("h3"))
