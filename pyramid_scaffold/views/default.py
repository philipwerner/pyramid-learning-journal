"""Views for the learning journal."""
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound
from pyramid_scaffold.models import Entry
from pyramid_scaffold.data.data import ENTRIES
import os


HERE = os.path.dirname(__file__)


@view_config(route_name='list', renderer='../templates/index.jinja2')
def list_view(request):
    """View for the listing of all journal entries."""
    entries = request.dbsession.query(Entry).all()
    entries = [entry.to_dict() for entry in entries]
    return {
        "page_title": "Phil's Learning Journal",
        "entries": entries,
    }


@view_config(route_name='detail', renderer='../templates/detail.jinja2')
def detail_view(request):
    """View config for the detailed view page."""
    entry_id = int(request.matchdict['id'])
    entry = request.dbsession.query(Entry).get(entry_id)
    if entry:
            return {
                "page_title": "Phil's Blog",
                "entry": entry.to_dict()
            }
    raise HTTPNotFound()


@view_config(route_name='create', renderer='../templates/new.jinja2')
def create_view(request):
    """View config for the new post view."""
    return{
        "page_title": "Create New Entry"
    }


@view_config(route_name='update', renderer='../templates/edit.jinja2')
def update_view(request):
    """View config for the edit post view."""
    entry_id = int(request.matchdict['id'])
    for entry in ENTRIES:
        if entry['id'] == entry_id:
            hero_title = "Edit Entry"
            return {
                "page_title": hero_title,
                "entry": entry
            }
    raise HTTPNotFound()
