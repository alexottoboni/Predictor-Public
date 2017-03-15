class User:
    def __init__(self, username, id, project_id, project_name):
        self.username = username
        self.id = id
        self.project_id = project_id
        self.project_name = project_name

    def __str__(self):
        return str(self.username + " " + self.project_id + " " + self.project_name + " " + self.id)
