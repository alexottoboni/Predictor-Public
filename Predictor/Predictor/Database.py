from project import Project
from Developer import Developer
from Issue import Issue
from ClassFile import ClassFile
from Pull import Pull
import MySQLdb
import sys

###
# Change password to what is set in Vagrantfile
pwd = "seniorproj"
###

class Database:
    class __Database:
        def __init__(self, host="localhost", user="root", passwd=pwd, db="seniorproject"):
            self.db = MySQLdb.connect(host = host, user = user,
                                      passwd = passwd, db = db,
                                      use_unicode=True, charset="utf8")
        def get_projects(self):
            cursor = self.db.cursor()
            sql_query = "select id from projects where id != -1"
            cursor.execute(sql_query)
            ids = []
            for row in cursor:
                ids.append(row[0])
            projects = []
            for id in ids:
                projects.append(self.get_project(id))
            return projects

        def get_pull(self, pull_id, project_id):
            cursor = self.db.cursor()
            sql_query = "select file_id from pull where id = %s and project = %s"
            cursor.execute(sql_query, (pull_id, project_id))
            file_ids = []
            for row in cursor:
                file_ids.append(row[0])
            file_objs = []
            for file_id in file_ids:
                file_objs.append(self.get_file(file_id, project_id))
            sql_query = "select id, body, dev_id, additions, deletions from pull where id = %s and project = %s"
            cursor.execute(sql_query, (pull_id, project_id))
            for row in cursor:
                return Pull(row[0], row[1], row[2], file_objs, row[3], row[4], project_id)

        def get_all_pulls(self, project_id):
            cursor = self.db.cursor()
            sql_query = "select DISTINCT id from pull where project = %s"
            cursor.execute(sql_query, (project_id,))
            ids = []
            for row in cursor:
                ids.append(row[0])
            pulls = []
            for id in ids:
                pulls.append(self.get_pull(id, project_id));
            return pulls

        def get_project(self, project_id):
            cursor = self.db.cursor()
            sql_query = "select id, name from projects where id = %s"
            cursor.execute(sql_query, (project_id,))
            for row in cursor:
                project = Project(project_id, row[1])
            reqs = self.get_all_reqs(project_id)
            devs = self.get_all_devs(project_id)
            files = self.get_all_files(project_id)
            pulls = self.get_all_pulls(project_id)
            project.classfiles = files
            project.devs = devs
            project.issues = reqs
            project.pulls = pulls
            return project

        def get_all_files(self, project_id):
            cursor = self.db.cursor()
            sql_query = "select id, name from class where project = %s"
            cursor.execute(sql_query, (project_id,))
            files = []
            for row in cursor:
                files.append(ClassFile(row[0], row[1], project_id))
            return files

        def get_file(self, file_id, project_id):
            cursor = self.db.cursor()
            sql_query = "select id, name from class where id = %s and project = %s"
            cursor.execute(sql_query, (file_id, project_id))
            for row in cursor:
                return ClassFile(row[0], row[1], project_id)

        def get_all_reqs(self, project_id):
            cursor = self.db.cursor()
            sql_query = "select id from req where project = %s"
            cursor.execute(sql_query, (project_id,))
            ids = []
            for row in cursor:
                ids.append(row[0])
            reqs = []
            for id in ids:
                reqs.append(self.get_req(id))
            return reqs;

        def get_all_cur_reqs(self, project):
            cursor = self.db.cursor()
            sql_query = "select id from req where project = %s and is_past = 0"
            cursor.execute(sql_query, (project,))
            ids = []
            for row in cursor:
                ids.append(row[0])
            reqs = []
            for id in ids:
                reqs.append(self.get_req(id))
            return reqs;

        def get_all_past_reqs(self, project):
            cursor = self.db.cursor()
            sql_query = "select id from req where project = %s and is_past = 1"
            cursor.execute(sql_query, (project,))
            ids = []
            for row in cursor:
                ids.append(row[0])
            reqs = []
            for id in ids:
                reqs.append(self.get_req(id))
            return reqs

        def get_req(self, req_id):
            cursor = self.db.cursor()
            sql_query = "select class_id, class_affinity from req where id = %s"
            cursor.execute(sql_query, (req_id,))
            mapping = {}
            for row in cursor:
                mapping[row[0]] = row[1]
            sql_query = "select id, title, description, project, created_at, closed_at, churn, is_past from req where id = %s"
            cursor.execute(sql_query, (req_id,))
            for row in cursor:
                return Issue(row[0], row[1], row[2], mapping, row[3], row[4], row[5], row[6], row[7])

        def get_all_devs(self, project_id):
            cursor = self.db.cursor()
            sql_query = "select id from dev where project = %s"
            cursor.execute(sql_query, (project_id,))
            ids = []
            for row in cursor:
                ids.append(row[0])
            devs = []
            for id in ids:
                devs.append(self.get_dev(id))
            return devs

        def get_dev(self, dev_id):
            cursor = self.db.cursor()
            sql_query = "select class_id, class_affinity from dev where id = %s"
            cursor.execute(sql_query, (dev_id,))
            mapping = {}
            for row in cursor:
                if row[0] != -1:
                    mapping[row[0]] = row[1]
            sql_query = "select id, name, project from dev where id = %s"
            cursor.execute(sql_query, (dev_id,))
            for row in cursor:
                return Developer(row[0], row[1], mapping, row[2])

        def delete_project(self, project_id):
            cursor = self.db.cursor()
            cursor.execute("delete from pull where project=%s", (project_id,));
            cursor.execute("delete from req where project=%s", (project_id,));
            cursor.execute("delete from dev where project=%s", (project_id,));
            cursor.execute("delete from class where project=%s", (project_id,));
            cursor.execute("delete from projects where id=%s", (project_id,));
            self.db.commit()

        def get_new_project_id(self):
            cursor = self.db.cursor()
            row_count = cursor.execute("select MAX(id) from projects;")
            # find a better way to check
            for row in cursor:
                try:
                    return int(row[0]) + 1
                except:
                    return 0

        def new_project(self, proj):
            cursor = self.db.cursor()
            cursor.execute("insert into projects (id, name) VALUES ("
                           + str(proj.id) + ", \"" + proj.name + "\");")
            self.db.commit()

        def new_pull(self, pull):
            print "in new Pull"
            try:
                cursor = self.db.cursor()
                sql_query = "insert into pull (id, body, dev_id, file_id, additions, deletions, project) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql_query, (pull.id, pull.body, pull.dev_id, "-1", "0", "0", pull.project_id))
                print (pull.id, pull.body, pull.dev_id, "-1", "0", "0", pull.project_id)
                print "commited"
                self.db.commit()
            except:
                print "Something went wrong creating a new pull"

        def new_issue(self, issue):
            cursor = self.db.cursor()
            if issue.class_affinity:
                for key, value in issue.class_affinity.items():
                    sql_query = "insert into req (id, title, description, class_id, class_affinity, project, churn, is_past, created_at, closed_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql_query, (issue.issue_id, issue.title, issue.desc, key, value, issue.project_id, issue.churn, issue.is_past, str(issue.created_at), str(issue.closed_at)))
                self.db.commit()
            else:
                sql_query = "insert into req (id, title, description, class_id, class_affinity, project, churn, is_past, created_at, closed_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql_query, (issue.issue_id, issue.title, issue.desc, "-1", "-1", issue.project_id, issue.churn, issue.is_past, str(issue.created_at), str(issue.closed_at)))

        def new_developer(self, dev):
            cursor = self.db.cursor()
            if dev.name == "None":
                dev.name = "Anonymous"
            for key, value in dev.class_affinity.items():
                sql_query = "insert into dev (id, name, class_id, class_affinity, project) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql_query, (dev.dev_id, dev.name, key, value, dev.project))
            if len(dev.class_affinity.keys()) == 0:
                sql_query = "insert into dev (id, name, class_id, class_affinity, project) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql_query, (dev.dev_id, dev.name, -1, -1, dev.project))
            self.db.commit()

        def new_file(self, file):
            cursor = self.db.cursor()
            sql_query = "insert into class (id, name, project) VALUES (%s, %s, %s)"
            cursor.execute(sql_query, (file.id, file.path, file.project))
            self.db.commit()

    instance = None
    def __init__(self, host="localhost", user="root", passwd=pwd, db="seniorproject"):
        if not Database.instance:
            Database.instance = Database.__Database(host, user, passwd, db)
        else:
            return None
    def __getattr__(self, name):
        return getattr(self.instance, name)
