from GWSUtils import *

settings = {}

class GWSSettings:

    def __init__(self):
        with open(".login", "r") as values:
            for value in values:
                #Not a comment
                if not value.startswith('#'):
                    #Remove trailing comments
                    SanitizeDescription(value)
                    keyVal = value.split('=')
                    credentials[keyVal[0]] = keyVal[1]
