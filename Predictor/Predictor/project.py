class Project:
    def __init__(self, id, name, description=None, language=None, classfiles=None, devs=None, issues=None, pulls = None):
        self.id = id
        self.name = name
        self.description = description
        self.classfiles = classfiles
        self.devs = devs
        self.issues = issues
        self.pulls = pulls
    def __str__(self):
        return str(self.id) + " " + str(self.name)
