#Requirements for github
import requests
import json
#Requirements for python-wordpress-xmlrpc
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods import taxonomies
from wordpress_xmlrpc.compat import xmlrpc_client
import datetime, xmlrpclib


'''
Accepts a list of strings
If a 'gistblog' string exists in the list, returns true
Else returns false
'''
def GistBlogExists(tags):
    if 'gistblog' in str(tags):
        return True
    else:
        return False

'''
Removes the gistblog hashtag from a list
and returns the remaining hashtags
'''
def RemoveGistBlog(tags):
        tags.remove('gistblog')
        return tags;

'''
Accepts a string
Extracts all hashtags out of that string into a list
Returns a list of all the hashtags

'''
def GetTags(description):
    #Get all the tags in the description
    tags = []
    for tag in description.split():
        if tag.startswith("#"):
            tags.append(tag.lstrip("#"))
    #Check if the gistblog tag exists and return
    return tags


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
Converts Time strings from the kind returned by the Gist API
to the kind that Wordpress/XMLRPC likes.
'''
def TimeSanitizer(str):
        #Replace T with a space
        value = str.replace("T", " ")
        #Remove the Z
        value = value.replace("Z", "")
        #Remove last three characters
        value = value[:-4]
        return value


'''
Removes tags and leading/trailing whitespaces.
'''
def SanitizeDescription(description):
            sanitized = description
            for tag in description.split():
                if tag.startswith("#"):
                    sanitized = sanitized.replace(tag, "")
            #Remove trailing whitespaces
            sanitized = sanitized.rstrip()
            return sanitized


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
wp = Client('http://ash.wine/xmlrpc.php', 'USERNAME', 'PASSWORD')


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
