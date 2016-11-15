from GWSUtils import *

'''
The GistPost Class.
'''
class GistPost:
    def __init__(self, title, url, tags, created_at, body):
        self.title = title
        self.url = url
        self.tags = tags
        self.created_at = created_at
        self.body = body



'''
The GistBody Class.
'''
class GistBody:
    def __init__(self, filename, body, link):
        self.filename = filename
        self.body = body
