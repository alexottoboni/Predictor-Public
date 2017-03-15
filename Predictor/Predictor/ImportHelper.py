from flask import render_template, session, request
from Predictor import app
from Database import Database
from project import Project
from Issue import Issue
from Developer import Developer
from Pull import Pull

###
# Change password to what is set in Vagrantfile
pwd = "seniorproj"
###
ISSUE_LIMIT = 5000
DEV_LIMIT = 500
PR_LIMIT = 1000
 
def import_project(repo_to_import):
    issues = []
    devs = []
    pulls = []
    my_db = Database()
    new_project = Project(my_db.get_new_project_id(), repo_to_import.name,
                          repo_to_import.description, repo_to_import.language)

    try:
        fetch_issues_github(repo_to_import.get_issues(state="all")[:ISSUE_LIMIT], issues, new_project)
        print "done issues"
        fetch_devs_github(repo_to_import.get_contributors()[:DEV_LIMIT], devs, new_project)
        print "done devs"
        fetch_pr_github(repo_to_import.get_pulls(state="closed")[:PR_LIMIT], {}, pulls, new_project)
        print "done pulls"
    except:
        print "Ran out of Github API requests"

    new_project.devs = devs
    new_project.issues = issues
    new_project.pulls = pulls

    # Add project to the database
    my_db.new_project(new_project)
    session['project_id'] = new_project.id
    session['project_name'] = repo_to_import.full_name

    for issue in new_project.issues:
        my_db.new_issue(issue)
    for dev in new_project.devs:
        my_db.new_developer(dev)
    for pull in new_project.pulls:
        my_db.new_pull(pull)

    return new_project

def fetch_issues_github(data_slice, issues, new_project):
    for issue in data_slice:
        if issue.state == "closed":
            state_enum = 1
        else:
            state_enum = 0
        print issue.number
        issues.append(Issue(issue.number, issue.title, 
                            issue.body, {}, new_project.id, 
                            issue.created_at, issue.closed_at,
                            is_past=state_enum))

def fetch_devs_github(data_slice, devs, new_project):
    for dev in data_slice:
        devs.append(Developer(dev.id, dev.name, {}, new_project.id))

def fetch_files_github(data_slice, files, pulls):
    for pr in data_slice:
        pulls.append(pr)
        for class_file in pr.get_files():
            files.add(class_file.filename)

def fetch_pr_github(data_slice, file_map, pulls, new_project):
    for pr in data_slice:
        new_pull = Pull(pr.id, pr.body, pr.user.id, [], pr.additions, pr.deletions, new_project.id)
        pulls.append(new_pull)

