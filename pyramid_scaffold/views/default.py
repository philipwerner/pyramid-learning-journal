"""Views for the learning journal."""
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPFound, HTTPBadRequest
from pyramid_scaffold.security import is_authenticated
from pyramid.security import remember, forget
from pyramid_scaffold.models import Entry


@view_config(route_name='list', renderer='templates/index.jinja2', require_csrf=False)
def list_view(request):
    """View for the listing of all journal entries."""
    entries = request.dbsession.query(Entry).order_by(Entry.creation_date.desc()).all()
    entries = [entry.to_dict() for entry in entries]
    return {
        "page_title": "Phil's Learning Journal",
        "entries": entries,
    }


@view_config(route_name='detail', renderer='templates/detail.jinja2', require_csrf=False)
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


@view_config(
    route_name='create',
    renderer='templates/new.jinja2',
    permission='secret',
    require_csrf=True
)
def create_view(request):
    """Create a new post and add it to the database."""
    if request.method == "GET":
        return{}

    if request.method == "POST":
        if not all([field in request.POST for field in ['title', 'body']]):
            raise HTTPBadRequest
        count = request.dbsession.query(Entry).count()
        new_entry = Entry(
            id=count + 1,
            title=request.POST['title'],
            body=request.POST['body'],
        )
        request.dbsession.add(new_entry)
        return HTTPFound(request.route_url('list'))


@view_config(
    route_name='update',
    renderer='templates/edit.jinja2',
    permission='secret',
    require_csrf=True
)
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


@view_config(
    route_name='delete',
    permission='secret',
    require_csrf=True
)
def delete_view(request):
    """Delete a entry."""
    entry_id = int(request.matchdict['id'])
    entry = request.dbsession.query(Entry).get(entry_id)
    if not entry:
        raise HTTPNotFound
    request.dbsession.delete(entry)
    return HTTPFound(request.route_url('list'))


@view_config(
    route_name='login',
    renderer='templates/login.jinja2',
    require_csrf=False
)
def login(request):
    """Will control log in to the journal."""
    if request.authenticated_userid:
        return HTTPFound(request.route_url('home'))
    if request.method == "GET":
        return {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if is_authenticated(username, password):
            headers = remember(request, username)
            return HTTPFound(request.route_url('list'), headers=headers)
        return {
            'error': 'Username/password combination was bad.'
        }


@view_config(route_name='logout')
def logout(request):
    """Let the user logout."""
    headers = forget(request)
    return HTTPFound(request.route_url('list'), headers=headers)
