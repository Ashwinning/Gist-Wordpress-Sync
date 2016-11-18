import operator
import requests
from GWSUtils import *
from GWSSettings import *
from GWSGist import *


'''
Posts Markdown to be parsed to the GitHub API
Returns the parsed HTML.
'''
def ParseMarkdown(text):
    url = "https://api.github.com/markdown/raw"
    headers = {
        'content-type': "text/x-markdown"
        }
    parameters = {'access_token': settings['GITHUB_ACCESS_TOKEN']}
    if not settings['GITHUB_ACCESS_TOKEN']:
        response = requests.request("POST", url, data=text, headers=headers)
    else:
        response = requests.request("POST", url, data=text, headers=headers, params=parameters)
    return response.text

'''
Given a URL, returns the raw text response.
Encoded in utf-8.
'''
def GetFile(url):
    request = requests.get(url)
    return request.text.encode('utf-8')

'''
Returns code wrapped in Markdown code tags ```
So that code can be parsed as markdown by the API
'''
def WrapCode(language, text):
    return '```'+language+'\n'+text+'\n```'


'''
Generates and adds the links to the files.
`body` is a List of `GistBody` Objects
'''
def BodyBuilder(body, url):
    text = ""

    #Sort body objects by filename
    body.sort(key=lambda x: x.filename)

    #Bool to track if document contains any Markdown
    markdownExists = False

    for thing in body:
        if thing.language == 'Markdown':
            markdownExists = True
            text += thing.content
            text += '\n'
            '''
            text += '<div class="gist-meta">'
            text += '<a target=_blank href="' + url + GenerateAnchor(thing.filename) + '">'+thing.filename+'</a>'
            text += '</div>'
            text += '\n'
            '''
        else:
            text += '<div class="gist-meta"><svg aria-hidden="true" class="octicon octicon-gist" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M7.5 5L10 7.5 7.5 10l-.75-.75L8.5 7.5 6.75 5.75 7.5 5zm-3 0L2 7.5 4.5 10l.75-.75L3.5 7.5l1.75-1.75L4.5 5zM0 13V2c0-.55.45-1 1-1h10c.55 0 1 .45 1 1v11c0 .55-.45 1-1 1H1c-.55 0-1-.45-1-1zm1 0h10V2H1v11z"></path></svg>&nbsp;&nbsp;'
            text += '<a href="' + url + GenerateAnchor(thing.filename) + '">'+thing.filename+'</a>'
            text += '</div>'
            text += '\n'
            text += thing.content
            text += '\n'

        #If markdown does not exist in body
        if not markdownExists:
            #Add title to top
            text = '<h1>' + thing.description + '</h1> \n' + text

        #Wrap in the gist div
        text = '<div class="gist markdown-body gist-file">' + text + '</div>'
    return text

def RenderMarkdown(gistPost):
    body = []
    #print(gistPost.item['files'])
    for file in gistPost.item['files']:
        language = gistPost.item['files'][file]['language']
        if (language == 'Markdown'):
            rawURL = gistPost.item['files'][file]['raw_url']
            dlFile = GetFile(rawURL)
            parsed = ParseMarkdown(dlFile)
            body.append(GistBody(file, gistPost.item['description'], parsed, language))
        else:
            rawURL = gistPost.item['files'][file]['raw_url']
            dlFile = GetFile(rawURL)
            wrap = WrapCode(language, dlFile)
            parsed = ParseMarkdown(wrap)
            body.append(GistBody(file, gistPost.item['description'], parsed,language))
    gistPost.body = BodyBuilder(body, gistPost.item['html_url'])
