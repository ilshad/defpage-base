from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render_to_response
from defpage.base.config import system_params
from defpage.base.transmission import TRANSMISSION_TYPES
from defpage.base import meta
from defpage.base import apps

def anonym_only(func):
    def wrapper(req):
        if req.user.authenticated:
            req.session.flash(u"You are authenticated already")
            return HTTPFound(location="/")
        return func(req)
    return wrapper

def empty(req):
    return {}

def forbidden(req):
    req.response.status = 403
    return {}

def unauthorized(req):
    req.response.status = 401
    return {}

def notfound(req):
    req.response.status = 404
    return {}

def default(req):
    if not req.user.authenticated:
        return render_to_response("defpage.base:templates/frontpage/unauthenticated.pt",
                                  {"login_url":system_params.login_url,
                                   "signup_url":system_params.signup_url},
                                  request=req)
    return render_to_response("defpage.base:templates/frontpage/authenticated.pt",
                              {}, request=req)

def add_collection(req):
    if req.POST.get("submit"):
        title = req.POST.get("title", u"").strip()
        if not title:
            req.session.flash(u"Title is required")
            return {}
        cid = meta.create_collection(req.user.userid, title)
        return HTTPFound(location="/collection/%s" % cid)
    return {}

def display_collection(req):
    cid = req.matchdict["name"]
    info = meta.get_collection(req.user.userid, cid)
    _source = info["source"]
    stypes  = apps.get_source_types()
    def get_stype(k):
        for i in stypes:
            if i["id"] == k:
                return i
    source = _source and get_stype(_source["type"])
    return {"title":info["title"],
            "source_title":source and source["title"],
            "count_documents":info["count_documents"],
            "count_transmissions":info["count_transmissions"]}

def delete_collection(req):
    cid = req.matchdict["name"]
    info = meta.get_collection(req.user.userid, cid)
    if req.POST.get("submit"):
        if req.POST.get("confirm"):
            meta.delete_collection(req.user.userid, cid)
            return HTTPFound(location="/")
    return {"info":info}

def collection_properties(req):
    cid = req.matchdict["name"]
    info = meta.get_collection(req.user.userid, cid)
    if req.POST.get("submit"):
        title = req.POST.get("title")
        if title:
            meta.edit_collection(req.user.userid, cid, title=title)
            return HTTPFound(location="/collection/%s" % cid)
    return {"info":info}

def collection_roles(req):
    return {}

def source_overview(req):
    cid = req.matchdict["name"]
    info = meta.get_collection(req.user.userid, cid)
    source = info["source"]
    stypes  = apps.get_source_types()
    def get_stype(k):
        for i in stypes:
            if i["id"] == k:
                return i
    configured = source and get_stype(source["type"])
    if req.POST.get("setup_source"):
        if source:
            url = configured["url"]
        else:
            stype_id = req.POST.get("source_type_id")
            stype = get_stype(stype_id)
            url = stype["url"]
        return HTTPFound(location=u"%s/collection/%s" % (url, cid))
    return {"source":source, "source_types":stypes, "configured":configured}

def transmission_overview(req):
    cid = req.matchdict["name"]
    info = meta.get_collection(req.user.userid, cid)
    if req.POST.get("create_transmission"):
        ttype_id = req.POST.get("transmission_type_id")
        return HTTPFound(location=u"/collection/%s/transmission/+/%s" % (cid, ttype_id))
    return {"transmission_types":TRANSMISSION_TYPES,
            "transmissions":meta.get_collection_transmissions(req.user.userid, cid)}

def add_transmission_rest(req):
    cid = req.matchdict["name"]
    if req.POST.get("submit"):
        description = req.POST.get("description")
        url = req.POST.get("base_url")
        atype = req.POST.get("authentication_type")
        secret = req.POST.get("auth_secret")
        username = req.POST.get("auth_username")
        password = req.POST.get("auth_password")
        if url and atype == "x-secret" and secret:
            data = {"type":"rest",
                    "description":description,
                    "params":{"url":url,
                              "authentication":{"type":"x-secret",
                                                "secret":secret}}}
        if url and atype == "basic" and username and password:
            data = {"type":"rest",
                    "description":description,
                    "params":{"url":url,
                              "authentication":{"type":"basic",
                                                "username":username,
                                                "password":password}}}
        else:
            data = None
        if data:
            meta.create_transmission(req.user.userid, cid, data)
            return HTTPFound(location=u"/collection/%s/transmission" % cid)
    return {}
