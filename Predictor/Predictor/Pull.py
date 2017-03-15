class Pull:
    def __init__(self, id, body, dev_id, files, additions, deletions, project_id):
        self.id = id
        self.body = body
        self.dev_id = dev_id
        self.files = files
        self.additions = additions
        self.deletions = deletions
        self.project_id = project_id

    def __str__(self):
        return str(self.body)
