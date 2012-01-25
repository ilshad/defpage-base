from defpage.lib.authentication import UserBase
from defpage.base.config import system_params
from defpage.base import meta

class User(UserBase):

    email = None
    collections = None

    def authenticate(self, request):
        super(User, self).authenticate(request,
                                       system_params.auth_session_cookie_name,
                                       system_params.sessions_url)

    def _authenticated(self, request, info):
        self.email = info['email']
        self.collections = meta.search_collections(self.user_id)

    def _unauthenticated(self, request):
        self.email = None
        self.collections = None
