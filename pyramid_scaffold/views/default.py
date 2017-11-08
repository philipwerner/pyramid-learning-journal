"""Views for the learning journal."""
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPFound, HTTPBadRequest
from pyramid_scaffold.models import Entry


@view_config(route_name='list', renderer='templates/index.jinja2')
def list_view(request):
    """View for the listing of all journal entries."""
    entries = request.dbsession.query(Entry).order_by(Entry.creation_date.desc).all()
    entries = [entry.to_dict() for entry in entries]
    return {
        "page_title": "Phil's Learning Journal",
        "entries": entries,
    }


@view_config(route_name='detail', renderer='templates/detail.jinja2')
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


@view_config(route_name='create', renderer='templates/new.jinja2')
def create_view(request):
    """Create a new post and add it to the database."""
    if request.method == "GET":
        return{}

    if request.method == "POST":
        if not all([field in request.POST for field in ['title', 'body']]):
            raise HTTPBadRequest
        new_entry = Entry(
            title=request.POST['title'],
            body=request.POST['body'],
        )
        request.dbsession.add(new_entry)
        return HTTPFound(request.route_url('list'))


@view_config(route_name='update', renderer='templates/edit.jinja2')
def update_view(request):
    """View and edit an existing entry and update the database."""
    entry_id = int(request.matchdict['id'])
    entry = request.dbsession.query(Entry).get(entry_id)
    if not entry:
        raise HTTPNotFound

    if request.method == "GET":
        return {
            'page_title': 'Edit Entry',
            'entry': entry.to_dict()
        }

    if request.method == "POST":
        entry.title = request.POST['title']
        entry.body = request.POST['body']
        request.dbsession.add(entry)
        request.dbsession.flush()
        return HTTPFound(request.route_url('detail'))


@view_config(route_name='delete')
def delete_view(request):
    """Delete a entry."""
    entry_id = int(request.matchdict['id'])
    entry = request.dbsession.query(Entry).get(entry_id)
    if not entry:
        raise HTTPNotFound
    request.dbsession.delete(entry)
    return HTTPFound(request.route_url('list'))
