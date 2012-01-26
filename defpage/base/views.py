from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render_to_response
from defpage.base.config import system_params
from defpage.base import meta

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
    return HTTPFound(location=system_params.login_url)

def default(req):
    if not req.user.authenticated:
        return render_to_response("defpage.base:templates/frontpage/unauthenticated.pt",
                                  {"login_url":system_params.login_url,
                                   "signup_url":system_params.signup_url},
                                  request=req)
    return render_to_response("defpage.base:templates/frontpage/authenticated.pt",
                              {}, request=req)

def create_collection(req):
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
    return {"info":info}

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
    return {}

def transmission_overview(req):
    return {}

def public_overview(req):
    return {}
