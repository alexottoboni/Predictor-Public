class ClassFile:
    def __init__(self, id, path, project):
        self.id = id
        self.path = path
        self.project = project

    def __str__(self):
        return "".join(self.id, self.path, self.project)
