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
Generates anchor tags for linking to files.
'''
def GenerateAnchor(filename):
    filename.lower()
    filename = filename.replace(" ", "-")
    filename = filename.replace(".", "-")
    value = '#file-'+filename
    return value
