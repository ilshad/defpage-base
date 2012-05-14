from pyramid.security import Everyone
from pyramid.security import Authenticated
from pyramid.security import Allow

class Root(object):

    __name__ = ""
    __parent__ = None

    __acl__ = [
        (Allow, Authenticated, "add_collection")
        ]

root = Root()

def get_root(req):
    return root
