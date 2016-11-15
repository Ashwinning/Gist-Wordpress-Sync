import requests

'''
Posts Markdown to be parsed to the GitHub API
Returns the parsed HTML.
'''
def ParseMarkdown(text):
    url = "https://api.github.com/markdown/raw"
    headers = {
        'content-type': "text/x-markdown"
        }
    response = requests.request("POST", url, data=text, headers=headers)
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
