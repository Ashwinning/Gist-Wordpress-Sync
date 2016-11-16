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
from GWSGist import *
from GWSUtils import *
from GWSSettings import *
from GWSMarkdown import *

#Initialize
gwsSettings = GWSSettings()
#print('settings = ' + str(settings))


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
wp = Client(settings['WORDPRESS_URL']+'/xmlrpc.php', settings['WORDPRESS_USERNAME'], settings['WORDPRESS_PASSWORD'])

print('Getting Wordpress Posts')
'''
Get all Wordpress posts (in batches of 20) from the specified category.
And add all the titles to the wordpressPosts list.
If no category is specified, then gets all posts, and does not categorize posts.
'''
wpOffset = 0
wpIncrement = 20
while True:
    posts = wp.call(GetPosts({'number': wpIncrement, 'offset': wpOffset}))
    if len(posts) == 0:
        print ('Imported ' + str(len(wordpressPosts)) + ' Wordpress posts.')
        break  # no more posts returned
    for post in posts:
        #if it's in the specified category, add it to the list
        if settings['WORDPRESS_CATEGORY'] in str(post.terms):
            wordpressPosts.append(post)
            print ('id : ' + post.id)
            print ('title : ' + post.title)
            fields = GetCustomFields(post.custom_fields)
            print ('gistid : ' + fields['gistid'])
            print ('---')
    wpOffset = wpOffset + wpIncrement


print('Getting Gists')
'''
Get all Gists (in batches of 20)
And add all the gists with #gistblog to the gistBlogs list.
'''
page = 1
offset = 0
increment = 20
while True:
    #Make HTTP request to GitHub API
    parameters = {'access_token': settings['GITHUB_ACCESS_TOKEN']}
    if not settings['GITHUB_ACCESS_TOKEN']:
        r = requests.get('http://api.github.com/users/'+settings['GITHUB_USERNAME']+'/gists?page='+str(page)+'&per_page='+str(increment))
    else:
        r = requests.get('http://api.github.com/users/'+settings['GITHUB_USERNAME']+'/gists?page='+str(page)+'&per_page='+str(increment), params=parameters)
    response = r.json()
    if str(response) == '[]':
        print('Imported ' + str(len(gistBlogs)) + ' Gists.')
        break  # no more posts returned

    for item in response:
        description = item['description']
        tags = GetTags(description)
        #if it's got the gistblog hashtag, add it to the list
        if GistBlogExists(tags):
            print (description)
            print ('---')
            #Save the description as the title
            #print ('tags : ' + str(tags))
            gistPost = GistPost(item['id'], description, item['html_url'], RemoveGistBlog(tags), item['created_at'], "", item['updated_at'], item)
            gistBlogs.append(gistPost)
    offset = offset + increment
    page += 1

'''
Remove all gistBlogs from list which already exist
If gistblogs exist without matching `updated_at` values, than means new versions exist,
delete the wordpress post so the new version can be uploaded.
'''
for wordpressPost in wordpressPosts:
    for gistBlog in gistBlogs:
        wpField = GetCustomFields(wordpressPost.custom_fields) #Gets the custom_fields in a dict
        #print (wpField)
        if gistBlog.id == wpField['gistid']:
            #Post already exists in wordpress
            if gistBlog.updated_at == wpField['updated_at']:
                #Exact post exists, remove it from our gistblog list
                gistBlogs.remove(gistBlog)
            else:
                #wordpressPost is older, delete it so we can add the latest one
                wp.call(DeletePost(wordpressPost.id))
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
    RenderMarkdown(gistBlog)
    post = WordPressPost()
    titleToPost = SanitizeDescription(gistBlog.title)
    post.title = titleToPost
    post.content = gistBlog.body
    post.terms_names = {
            'post_tag': gistBlog.tags,
            'category': ['hacks'],
    }
    post.custom_fields = []
    post.custom_fields.append({
        'key': 'updated_at',
        'value': gistBlog.updated_at
        })
    post.custom_fields.append({
        'key': 'gistid',
        'value': gistBlog.id
        })
    post.post_status = 'publish'
    timestamp = TimeSanitizer(gistBlog.created_at)
    post.date = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M")
    post.id = wp.call(NewPost(post))
    gistsPosted += 1
    print (str(gistsPosted) + ') ' + titleToPost + ' posted.')
print ('COMPLETE! ' + str(gistsPosted) + ' new gists posted.')
