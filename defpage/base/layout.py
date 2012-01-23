from pyramid.renderers import get_renderer
from defpage.base.config import system_params
from defpage.base.interfaces import IUser

def top(context, req, view):
    snippets = []
    user = req.registry.getUtility(IUser)
    if user.user_id:
        snippets.append(u'<span id="usertitle">%s</span>' % user.email)
        snippets.append(u'<a href="%s">Logout</a>' % system_params.logout_url)
    else:
        snippets.append(u'<a href="%s">Login</a>' % system_params.login_url)
    return snippets

def renderer_add_globals(e):
    e["layout"] = get_renderer("defpage.base:templates/layout.pt").implementation()
    e["static_url"] = system_params.static_url
    e["user"] = e["request"].registry.getUtility(IUser)
    e["login_url"] = system_params.login_url
    e["logout_url"] = system_params.logout_url
    e["accounts_url"] = system_params.accounts_url
