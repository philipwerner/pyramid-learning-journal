"""To configure and hold all pertinent security information for the app."""
import os
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Authenticated
from pyramid.security import Allow
from pyramid.session import SignedCookieSessionFactory
from passlib.apps import custom_app_context as pwd_context


class MyRoot(object):
    """Set security permissions for authenticated users."""

    def __init__(self, requset):
        """Set starting variable."""
        self.requset = requset

    __acl__ = [
        (Allow, Authenticated, 'secret'),
    ]


def is_authenticated(username, password):
    """Check for proper username and password."""
    if username == os.environ.get('AUTH_USERNAME', ''):
        if pwd_context.verify(password, os.environ.get('AUTH_PASSWORD', '')):
            return True
    return False


def includeme(config):
    """Config for security stuffs."""
    auth_secret = os.environ.get('AUTH_SECRET', '')
    authn_policy = AuthTktAuthenticationPolicy(
        secret=auth_secret,
        hashalg='sha512'
    )
    session_secret = os.environ.get('SESSION_SECRET', 'itsaseekrit')
    session_factory = SignedCookieSessionFactory(session_secret)
    config.set_session_factory(session_factory)
    config.set_default_csrf_options(require_csrf=True)
    authz_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(authz_policy)
    config.set_root_factory(MyRoot)
