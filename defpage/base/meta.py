import json
import httplib2
from pyramid.httpexceptions import HTTPNotFound
from defpage.base.exceptions import ServiceCallError
from defpage.base.config import system_params

def search_collections(userid):
    h = httplib2.Http()
    r, c = h.request(system_params.meta_url + "/collections/?user_id=" + str(userid))
    if r.status == 200:
        return json.loads(c)
    elif r.status == 400:
        return []
    raise ServiceCallError

def create_collection(title, userid):
    h = httplib2.Http()
    r, c = h.request(system_params.meta_url + "/collections/", "POST", json.dumps({"title":title, "acl":{userid:["owner"]}}))
    if r.status == 201:
        r = json.loads(c)
        return r["id"]
    raise ServiceCallError

def get_collection(cid):
    h = httplib2.Http()
    r, c = h.request(system_params.meta_url + "/collections/" + str(cid))
    if r.status == 200:
        return json.loads(c)
    elif r.status == 404:
        raise HTTPNotFound
    raise ServiceCallError

def edit_collection(cid, **kw):
    h = httplib2.Http()
    r, c = h.request(system_params.meta_url + "/collections/" + str(cid), "PUT", json.dumps(kw))
    if r.status != 204:
        raise ServiceCallError
