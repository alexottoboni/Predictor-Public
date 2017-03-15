class Developer:
    def __init__(self, dev_id, name, class_affinity, project):
        self.dev_id = dev_id
        self.name = name
        self.class_affinity = class_affinity
        self.project = project

    def __str__(self):
        return u" ".join((str(self.dev_id), self.name, str(self.class_affinity))).encode('utf-8')
