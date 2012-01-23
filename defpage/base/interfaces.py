from zope.interface import Interface
from zope.interface import Attribute

class IUser(Interface):
    """User info from authenticated session. This interface is implemented
    by global utility (thread local). When a new request starts, we must
    authenticate the request by updating IUser utility's attributes. If
    the request is not authenticated then the attributes are None.

    The general goal of creating this utility is avoid multiple calls
    to security service within one request.
    """

    user_id = Attribute("User id")
    email = Attribute("Email")

    def authenticate(request):
        """Update attributes in new request"""
