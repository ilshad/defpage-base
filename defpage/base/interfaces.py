from zope.interface import Interface
from zope.interface import Attribute

class IUser(Interface):
    """User info for authenticated user.
    """

    authenticated = Attribute("Boolean")

    user_id = Attribute("User id")
    email = Attribute("Email")
    collections = Attribute("Collections")

    def authenticate(request):
        """Update attributes in new request"""
