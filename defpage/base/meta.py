import json
import httplib2
from pyramid.httpexceptions import HTTPNotFound
from defpage.base.exceptions import ServiceCallError
from defpage.base.config import system_params

def search_collections(userid):
    url = system_params.meta_url + "/collections/?user_id=" + str(userid)
    h = httplib2.Http()
    r, c = h.request(url)
    if r.status == 200:
        return json.loads(c)
    elif r.status == 400:
        return []
    raise ServiceCallError

def create_collection(title, userid):
    url = system_params.meta_url + "/collections/"
    body = json.dumps({"title":title, "acl":{userid:["owner"]}})
    h = httplib2.Http()
    r, c = h.request(url, "POST", body)
    if r.status == 201:
        r = json.loads(c)
        return r["id"]
    raise ServiceCallError

def get_collection(cid):
    url = system_params.meta_url + "/collections/" + str(cid)
    h = httplib2.Http()
    r, c = h.request(url)
    if r.status == 200:
        return json.loads(c)
    elif r.status == 404:
        raise HTTPNotFound
    raise ServiceCallError
