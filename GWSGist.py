from GWSUtils import *

'''
The GistPost Class.
'''
class GistPost:
    def __init__(self, id, title, url, tags, created_at, body, updated_at, item):
        self.id = id
        self.title = title
        self.url = url
        self.tags = tags
        self.created_at = created_at
        self.body = body
        self.updated_at = updated_at
        self.item = item



'''
The GistBody Class.
'''
class GistBody:
    def __init__(self, filename, content):
        self.filename = filename
        self.content = content
