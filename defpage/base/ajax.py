from defpage.base import meta

def get_collection_documents(req):
    docs = []
    for i in meta.get_collection_documents(req.user.usrid, req.matchdict["name"]):
        docs.append({"id":           i["id"],
                     "title":        i["title"],
                     "source_css":   i["source"]["type"] == "gd" and "source_css_gd"})
    return docs
