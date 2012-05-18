TRANSMISSION_TYPES = [
    {"id":"rest",    "title":u"REST API"},
    {"id":"dirty",   "title":u"Dirty API"}
    ]

def get_transmission_title(id):
    for i in TRANSMISSION_TYPES:
        if i["id"] == id:
            return i["title"]
