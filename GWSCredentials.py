class GWSLogin:

    def __init__(self):
        fo = open(".login", "r")
        self.username = fo.readline()
        self.password = fo.readline()
