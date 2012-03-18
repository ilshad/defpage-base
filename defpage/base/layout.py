from pyramid.renderers import get_renderer
from defpage.base.config import system_params

def renderer_add_globals(e):
    e["layout"] = get_renderer("defpage.base:templates/layout.pt").implementation()
    e["static_url"] = system_params.static_url
    e["login_url"] = system_params.login_url
    e["logout_url"] = system_params.logout_url
    e["accounts_url"] = system_params.accounts_url
    e["help_url"] = system_params.help_url
    e["active_collection_id"] = active_collection(e["request"])

def active_collection(req):
    segments = req.path.split("/")
    if segments[1] == "collection":
        try:
            return int(segments[2])
        except:
            return None
    return None
