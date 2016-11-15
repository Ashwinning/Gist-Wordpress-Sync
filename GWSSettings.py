from GWSUtils import *

settings = {}

class GWSSettings:
    settings = {}
    def __init__(self):
        with open(".settings", "r") as values:
            for value in values:
                value.strip() #Remove whitespaces
                #Not a comment, not just a linebreak
                if not(value.startswith('#') or (value in ['\n', '\r\n'])):
                    #print ('Found Line : ' + value)
                    #Remove trailing comments
                    SanitizeDescription(value)
                    keyVal = value.split('=')
                    settings[keyVal[0]] = keyVal[1].strip()
                    #print(keyVal[0] + ' ' + settings[keyVal[0]])
