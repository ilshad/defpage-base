import json
import base64
import httplib2
from pyramid.httpexceptions import HTTPNotFound
from pyramid.httpexceptions import HTTPUnauthorized
from defpage.lib.exceptions import ServiceCallError
from defpage.base.config import system_params

def auth_headers(userid):
    return {"Authorization":"Basic " + base64.b64encode(str(userid or "") + ":1")}

def search_collections(userid):
    h = httplib2.Http()
    headers = auth_headers(userid)
    r, c = h.request(system_params.meta_url + "/collections/?user_id=" + str(userid),
                     headers=headers)
    if r.status == 200:
        return json.loads(c)
    elif r.status == 400:
        return []
    elif r.status == 401 or r.status == 403:
        raise HTTPUnauthorized
    raise ServiceCallError

def create_collection(title, userid):
    h = httplib2.Http()
    headers = auth_headers(userid)
    body = json.dumps({"title":title, "owner":userid})
    r, c = h.request(system_params.meta_url + "/collections/",
                     method="POST",
                     body=body,
                     headers=headers)
    if r.status == 201:
        r = json.loads(c)
        return r["id"]
    elif r.status == 401 or r.status == 403:
        raise HTTPUnauthorized
    raise ServiceCallError

def get_collection(cid, userid):
    h = httplib2.Http()
    headers = auth_headers(userid)
    r, c = h.request(system_params.meta_url + "/collections/" + str(cid),
                     method="GET",
                     headers=headers)
    if r.status == 200:
        return json.loads(c)
    elif r.status == 404:
        raise HTTPNotFound
    elif r.status == 401 or r.status == 403:
        raise HTTPUnauthorized
    raise ServiceCallError

def edit_collection(cid, userid, **kw):
    h = httplib2.Http()
    headers = auth_headers(userid)
    body = json.dumps(kw)
    r, c = h.request(system_params.meta_url + "/collections/" + str(cid),
                     method="PUT",
                     body=body,
                     headers=headers)
    if r.status == 401 or r.status == 403:
        raise HTTPUnauthorized
    elif r.status != 204:
        raise ServiceCallError

def delete_collection(cid, userid):
    h = httplib2.Http()
    headers = auth_headers(userid)
    r, c = h.request(system_params.meta_url + "/collections/" + str(cid),
                     method="DELETE",
                     headers=headers)
    if r.status == 401 or r.status == 403:
        raise HTTPUnauthorized
    elif r.status != 204:
        raise ServiceCallError
