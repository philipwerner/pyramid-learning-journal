"""Views for the learning journal."""
from pyramid.view import view_config
from pyramid_scaffold.data.data import ENTRIES
from pyramid.httpexceptions import HTTPNotFound
import os


HERE = os.path.dirname(__file__)


@view_config(route_name='list', renderer='../templates/index.jinja2')
def list_view(request):
    """View for the listing of all journal entries."""
    new_entries = reversed(ENTRIES)
    return {
        "page_title": "Phil's Learning Journal",
        "entries": new_entries,
    }


@view_config(route_name='detail', renderer='../templates/detail.jinja2')
def detail_view(request):
    """View config for the detailed view page."""
    the_id = int(request.matchdict['id'])

    for entry in ENTRIES:
        if entry['id'] == the_id:
            hero_title = "Journal Post"
            title = "Phil\'s Blog - {}".format(entry["title"])
            return {
                "page_title": hero_title,
                "entry": entry,
                "title": title,
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
