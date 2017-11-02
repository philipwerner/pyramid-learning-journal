"""Tests for learning journal app."""

from pyramid.testing import DummyRequest
from pyramid import testing
from pyramid.response import Response


def test_list_view_returns_response_object():
    """Will test for a response object."""
    from pyramid_scaffold.views import list_view
    req = DummyRequest()
    response = list_view(req)
    assert isinstance(response, Response)


def test_list_view_returns_status_200():
    """Tests for a 200 status."""
    from pyramid_scaffold.views import list_view
    req = DummyRequest()
    response = list_view(req)
    assert response.status_code == 200


def test_list_view_content_is_correct():
    """Tests for proper content on homepage."""
    from pyramid_scaffold.views import list_view
    req = DummyRequest()
    response = list_view(req)
    assert "Phil's Blog" in response.text


def test_detail_view_returns_response_object():
    """Tests for proper content on detail page."""
    from pyramid_scaffold.views import detail_view
    req = DummyRequest()
    response = detail_view(req)
    assert isinstance(response, Response)


def test_detail_view_returns_status_200():
    """Tests for a 200 response from the detail page."""
    from pyramid_scaffold.views import detail_view
    req = DummyRequest()
    response = detail_view(req)
    assert response.status_code == 200


def test_detail_view_content_is_correct():
    """Tests for proper content on the detail page."""
    from pyramid_scaffold.views import detail_view
    req = DummyRequest()
    response = detail_view(req)
    assert "Man must explore, and this is exploration at its greatest" in response.text


def test_create_view_returns_response_object():
    """Tests for a 200 response frome the create page."""
    from pyramid_scaffold.views import create_view
    req = DummyRequest()
    response = create_view(req)
    assert isinstance(response, Response)



def test_create_view_content_is_correct():
    """Tests for proper content on create page."""
    from pyramid_scaffold.views import create_view
    req = DummyRequest()
    response = create_view(req)
    assert "New Article" in response.text


def test_update_view_returns_response_object():
    """Tests for a response object from the update/edit page."""
    from pyramid_scaffold.views import update_view
    req = DummyRequest()
    response = update_view(req)
    assert isinstance(response, Response)


def test_update_view_returns_status_200():
    """Tests for a 200 response from the update/edit page."""
    from pyramid_scaffold.views import update_view
    req = DummyRequest()
    response = update_view(req)
    assert response.status_code == 200


def test_update_view_content_is_correct():
    """Tests for proper content from the update/edit page."""
    from pyramid_scaffold.views import update_view
    req = DummyRequest()
    response = update_view(req)
    assert "Edit Entry" in response.text
