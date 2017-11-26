"""To configure and hold all pertinent security information for the app."""
import os
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Authenticated, Everyone
from pyramid.security import Allow
from pyramid.session import SignedCookieSessionFactory
from passlib.apps import custom_app_context as pwd_context


class MyRoot(object):
    """Set security permissions for authenticated users."""

    def __init__(self, requset):
        """Set starting variable."""
        self.requset = requset

    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, 'secret'),
    ]


def is_authenticated(username, password):
    """Check for proper username and password."""
    stored_username = os.environ.get('AUTH_USERNAME', '')
    stored_password = os.environ.get('AUTH_PASSWORD', '')
    is_authenticated = False
    if stored_username and stored_password:
        if username == stored_username:
            try:
                is_authenticated = pwd_context.verify(password, stored_password)
            except ValueError:
                pass
    return is_authenticated


def includeme(config):
    """Config for security stuffs."""
    auth_secret = os.environ.get('AUTH_SECRET', 'itsaseekrit')
    session_factory = SignedCookieSessionFactory(auth_secret)
    config.set_session_factory(session_factory)
    config.set_default_csrf_options(require_csrf=True)
    authn_policy = AuthTktAuthenticationPolicy(
        secret=auth_secret,
        hashalg='sha512'
    )
    config.set_authentication_policy(authn_policy)
    authz_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(authz_policy)
    config.set_root_factory(MyRoot)
