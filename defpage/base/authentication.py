import json
import httplib2
from zope.interface import implementer
from pyramid.interfaces import IAuthenticationPolicy
from defpage.base.exceptions import ServiceCallError
from defpage.base.config import system_params
from defpage.base.interfaces import IUser
from defpage.base import meta

def authenticate(event):
    user = event.request.registry.getUtility(IUser)
    user.authenticate(event.request)

@implementer(IUser)
class User(object):

    authenticated = False

    user_id = None
    email = None
    collections = None

    def authenticate(self, request):
        key = request.cookies.get(system_params.auth_session_cookie_name)
        if key:
            url = system_params.sessions_url + key
            h = httplib2.Http()
            response, content = h.request(url)
            if response.status == 200:
                info = json.loads(content)
                self.user_id = info['user_id']
                self.email = info['email']
                self.collections = meta.search_collections(self.user_id)
                self.authenticated = True
                return
            elif response.status != 404:
                raise ServiceCallError
        self.authenticated = False
        self.user_id = None
        self.email = None
        self.collections = None

@implementer(IAuthenticationPolicy)
class AuthenticationPolicy(object):

    def authenticated_userid(self, request):
        user = request.registry.getUtility(IUser)
        return user.user_id

    def unauthenticated_userid(self, request):
        return None

    def effective_principals(self, request):
        return [self.authenticated_userid(request)]

    def remember(self, request, principal, email):
        return []

    def forget(self, request):
        return []
