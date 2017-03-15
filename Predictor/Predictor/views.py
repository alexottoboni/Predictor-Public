from flask import render_template, session, request
from Predictor import app
from project import Project
from Database import Database
from Issue import Issue
from Developer import Developer
from Pull import Pull
from github import Github
from TextualSimilarity import TextualSimilarity 
import ImportHelper
import PredictionHelper

GITHUB_USER = ""
GITHUB_PASSWORD = ""

@app.route("/")
def index():
    if 'project_name' in session.keys() and 'project_id' in session.keys():
        return render_template('index.html', title='Home', project_name=session['project_name'])
    else:
        return render_template('index.html', title='Home', project_name="No Project Selected")

@app.route("/devs")
def select_devs():
    if 'project_id' in session.keys():
        db = Database()
        devs = db.get_all_devs(session['project_id'])
        return render_template('devs.html', title="Select Devs", devs=devs)
    else:
        return "Select a project first"

@app.route("/switch", methods=['GET', 'POST'])
def switch_project():
    db = Database()
    if request.method == "GET":
        projects = db.get_projects()
        return render_template("switch.html", title="Select Project", projects=projects)
    else:
        project = db.get_project(request.form["project"])
        session["project_id"] = project.id
        session["project_name"] = project.name
        return render_template("index.html", title="Home", project_name=project.name)

@app.route("/issues")
def select_issues():
    db = Database()
    issues = db.get_all_reqs(session["project_id"])
    return render_template('issues.html', title="Select Devs", issues=issues)

@app.route("/results")
def display_results():
    reqs = request.args.get('reqs')
    reqs = reqs.split(',')
    devs = request.args.get('devs')
    devs = devs.split(',')
    mapping = PredictionHelper.match_dev_to_issue(devs, reqs)
    return render_template("results.html", title="Results", mapping=mapping)

@app.route("/reset")
def reset_project():
    if "project_id" not in session.keys():
        return "Select a project first"
    my_db = Database()
    my_db.delete_project(session["project_id"])
    project_name = session["project_name"]
    session.clear()
    return "Deleted " + project_name

@app.route("/stats")
def stats():
    correct = PredictionHelper.compute_all_debug()[1]
    result = str(correct[0]) + " " + str(correct[1]) + " " + str(correct[2]) + " " + str(correct[3])
    result += " Out of " + str(correct[4])
    return result

@app.route("/csv_data")
def csv_data():
    return PredictionHelper.compute_all_debug()[2]

@app.route("/projects", methods=['GET', 'POST'])
def manage_projects():
    if request.method == 'POST':
        issues = []
        devs = []
        pulls = []
        files = set()
        g = Github(GITHUB_USER, GITHUB_PASSWORD)

        if request.form['project'] == "custom_project":
            repo_to_import = g.get_repo(request.form['other'])
        else:
            for repo in g.get_user().get_repos():
                if repo.full_name == request.form['project']:
                    repo_to_import = repo
                else:
                    return "Error fetching repo" + str(request.form['project'])

        new_project = ImportHelper.import_project(repo_to_import)
        
        return "Finished Importing " + new_project.name + " with " + str(len(new_project.issues)) + " issues, " + str(len(new_project.devs)) + " devs, and" + str(len(new_project.pulls)) + " pulls"
    else:
        g = Github(GITHUB_USER, GITHUB_PASSWORD)
        projects = []
        for repo in g.get_user().get_repos():
            projects.append(repo)
        return render_template("projects.html", projects=projects)
