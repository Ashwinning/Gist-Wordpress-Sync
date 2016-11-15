class GWSLogin:

    credentials = {}

    def __init__(self):
        with open(".login", "r") as values:
            for value in values:
                keyVal = credential.split('=')
                credentials[keyVal[0]] = keyVal[1]
        self.WORDPRESS_USERNAME = credentials['WORDPRESS_USERNAME']
        self.WORDPRESS_PASSWORD = credentials['WORDPRESS_PASSWORD']
        self.GITHUB_USERNAME = credentials['GITHUB_USERNAME']
        self.WORDPRESS_URL = credentials['WORDPRESS_URL']
