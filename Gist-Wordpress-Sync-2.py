#Requirements for github
import requests
import json
#Requirements for python-wordpress-xmlrpc
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods import taxonomies
from wordpress_xmlrpc.compat import xmlrpc_client
import datetime, xmlrpclib

#Project files
from GWSUtils import *
from GWSSettings import GWSSettings

#Initialize
gwsSettings = GWSSettings()

'''
The GistPost Class.
'''
class GistPost:
    def __init__(self, title, url, tags, created_at):
        self.title = title
        self.url = url
        self.tags = tags
        self.created_at = created_at


'''
A list of all the tagged gists
'''
gistBlogs = []


'''
A list of all the Wordpress Posts
'''
wordpressPosts = []


'''
Create the Wordpress Client which will retrieve and post posts
'''
wp = Client(gwsLogin.WORDPRESS_URL+'/xmlrpc.php', gwsLogin.WORDPRESS_USERNAME, gwsLogin.WORDPRESS_PASSWORD)


'''
Get all Wordpress posts (in batches of 20) from the Hacks category
And add all the titles to the wordpressPosts list.
'''
wpOffset = 0
wpIncrement = 20
while True:
        posts = wp.call(GetPosts({'number': wpIncrement, 'offset': wpOffset}))
        if len(posts) == 0:
                print ('Imported ' + str(len(wordpressPosts)) + ' Wordpress posts.')
                break  # no more posts returned
        for post in posts:
                #if it's in the hacks category, add it to the list
                if 'Hacks' in str(post.terms):
                    wordpressPosts.append(post)
        wpOffset = wpOffset + wpIncrement

'''
Get all Gists (in batches of 20)
And add all the gists with #gistblog to the gistBlogs list.
'''
page = 1
offset = 0
increment = 20
while True:
        #Make HTTP request to GitHub API
        r = requests.get('http://api.github.com/users/ashwinning/gists?page='+str(page)+'&per_page='+str(increment))
        response = r.json()
        if str(response) == '[]':
                print('Imported ' + str(len(gistBlogs)) + ' Gists.')
                break  # no more posts returned
        for item in response:
                description = item['description']
                tags = GetTags(description)
                #if it's got the gistblog hashtag, add it to the list
                if GistBlogExists(tags):
                        #Save the description as the title
                        gistPost = GistPost(description, item['html_url'], RemoveGistBlog(tags), item['created_at'])
                        gistBlogs.append(gistPost)
        offset = offset + increment
        page += 1


'''
Remove all gistBlogs from list which already exist
in wordpressPosts
'''
for wordpressPost in wordpressPosts:
        for gistBlog in gistBlogs:
                if wordpressPost.title in gistBlog.title:
                        #Remove this gistblog
                        gistBlogs.remove(gistBlog)
                        break #Move to next wordpressPost


'''
Display the number of gists to be posted
'''
print ('Posting ' + str(len(gistBlogs)) + ' new gists.')


'''
Post remaining gistBlogs to Wordpress
'''
gistsPosted = 0
for gistBlog in gistBlogs:
        post = WordPressPost()
        titleToPost = SanitizeDescription(gistBlog.title)
        post.title = titleToPost
        post.content = gistBlog.url
        post.terms_names = {
                'post_tag': gistBlog.tags,
                'category': ['hacks'],
        }
        post.post_status = 'publish'
        timestamp = TimeSanitizer(gistBlog.created_at)
        post.date = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M")
        #post.id = wp.call(NewPost(post))
        gistsPosted += 1
        print (str(gistsPosted) + ') ' + titleToPost + ' posted.')
print ('COMPLETE! ' + str(gistsPosted) + ' new gists posted.')
