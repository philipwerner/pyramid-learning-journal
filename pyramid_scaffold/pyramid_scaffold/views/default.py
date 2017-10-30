"""."""


from pyramid.response import Response
import os

HERE = os.path.dirname(__file__)


def list_view(request):
    """."""
    with open("pyramid_scaffold/templates/index.html") as file:
        return Response(file.read())


def detail_view(request):
    """."""
    with open("pyramid_scaffold/templates/detail.html") as file:
        return Response(file.read())


def create_view(request):
    """."""
    with open("pyramid_scaffold/templates/new.html") as file:
        return Response(file.read())


def update_view(request):
    """."""
    with open("pyramid_scaffold/templates/edit.html") as file:
        return Response(file.read())
