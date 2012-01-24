import json
import httplib2
from defpage.lib.exceptions import ServiceCallError
from defpage.base.config import system_params

def sendmail(recipients, subject, body):
    url = system_params.mail_url
    content = json.dumps({'recipients':recipients, 'subject':subject, 'body':body})
    headers = {'Content-Type':'application/json'}
    h = httplib2.Http()
    response, _c = h.request(url, "POST", content, headers)
    if response.status != 202:
        raise ServiceCallError
