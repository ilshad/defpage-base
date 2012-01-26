import json
import base64
import httplib2
from pyramid.httpexceptions import HTTPNotFound
from pyramid.httpexceptions import HTTPUnauthorized
from defpage.lib.exceptions import ServiceCallError
from defpage.base.config import system_params

def _call(userid, url, method, body=None, headers={}):
    h = httplib2.Http()
    headers.update({"Authorization":"Basic " + base64.b64encode(str(userid or "") + ":1")})
    r, c = h.request(system_params.meta_url + url, method=method, body=body, headers=headers)
    if r.status == 401 or r.status == 403:
        raise HTTPUnauthorized
    return r, c

def search_collections(userid):
    r,c = _call(userid, "/collections/?user_id=" + str(userid), "GET", None)
    if r.status == 200:
        return json.loads(c)
    elif r.status == 400:
        return []
    raise ServiceCallError

def create_collection(userid, title):
    r,c = _call(userid, "/collections/", "POST", json.dumps({"title":title, "owner":userid}))
    if r.status == 201:
        r = json.loads(c)
        return r["id"]
    raise ServiceCallError

def get_collection(userid, cid):
    r,c = _call(userid, "/collections/" + str(cid), "GET", None)
    if r.status == 200:
        return json.loads(c)
    elif r.status == 404:
        raise HTTPNotFound
    raise ServiceCallError

def edit_collection(userid, cid, **kw):
    r,c = _call(userid, "/collections/" + str(cid), "PUT", json.dumps(kw))
    if r.status != 204:
        raise ServiceCallError

def delete_collection(userid, cid):
    r,c = _call(userid, "/collections/" + str(cid), "DELETE", None)
    if r.status != 204:
        raise ServiceCallError
