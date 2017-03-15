class Issue:
    def __init__(self, issue_id, title, desc, class_affinity, project_id, created_at, closed_at, churn=0, is_past=True):
        self.issue_id = issue_id
        self.title = title
        self.desc = desc
        self.class_affinity = class_affinity
        self.issue_id = issue_id
        self.project_id = project_id
        self.created_at = created_at
        self.closed_at = closed_at
        self.churn = churn
        self.is_past = is_past
    
    def __str__(self):
        return u" ".join((str(self.issue_id), self.title, self.desc,
                         str(self.class_affinity), str(self.issue_id), str(self.project_id))).encode('utf-8')
