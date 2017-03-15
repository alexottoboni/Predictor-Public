from flask import render_template, session, request
from Predictor import app
from Database import Database
from project import Project
from Issue import Issue
from Developer import Developer
from Pull import Pull
from TextualSimilarity import TextualSimilarity 

def match_dev_to_issue(devs, issue_ids):
    my_db = Database()
    cur_project = my_db.get_project(session['project_id'])
    dev_corpus = build_corpus(cur_project)
    issues_to_select = []
    dev_objs = []
    for dev in devs:
        dev_objs.append(my_db.get_dev(dev))

    for id in issue_ids:
        tmp_issue = issue_from_id(id, cur_project)
        if tmp_issue:
            issues_to_select.append(tmp_issue)
    mapping = {}
    ts = TextualSimilarity()

    for cur_dev in dev_objs:
        best_guesses = []
        worst_guesses = []
        avg_guesses = []
        for open_issue in issues_to_select:
            cur_text = str(open_issue.desc + " " + open_issue.title)

            # Compute good similarity
            corpus = str(dev_corpus[cur_dev.dev_id]["good"])
            homebrew_good = ts.homebrew_nlp(cur_text, corpus) * 100
            leven_good = ts.levenshtein(cur_text, corpus) * 100
            cosine_good = ts.cosine_test(cur_text, corpus) * 100
            best_guesses.append((homebrew_good, leven_good, cosine_good, open_issue))
            
            # Compute bad similarity
            corpus = str(dev_corpus[cur_dev.dev_id]["bad"])
            homebrew_bad = ts.homebrew_nlp(cur_text, corpus) * 100
            leven_bad = ts.levenshtein(cur_text, corpus) * 100
            cosine_bad = ts.cosine_test(cur_text, corpus) * 100
            worst_guesses.append((homebrew_good, leven_good, cosine_good, open_issue))
    
            avg_guesses.append((homebrew_good - homebrew_bad, 
                             leven_good - leven_bad,
                             cosine_good - cosine_bad, open_issue))
            
        best_guess = sorted(best_guesses, key=lambda x: x[0], reverse=True)
        worst_guess = sorted(worst_guesses, key=lambda x: x[0], reverse=True)
        avg_guess = sorted(avg_guesses, key=lambda x: x[0], reverse=True)
        mapping[cur_dev] = avg_guess
    return mapping

def compute_all_debug():
    # Output Data Fields
    csv = ""
    debug = ""

    # Setup Data
    if "project_id" not in session.keys():
        return "Select a project first"
    my_db = Database()
    cur_project = my_db.get_project(session['project_id'])
    ts = TextualSimilarity()

    # Link pulls to issues
    pull_to_issue = build_pull_to_issue_map(cur_project)
    issue_to_pull = build_issue_to_pull_map(cur_project)
    linked_issues = []
    for pull in cur_project.pulls:
        print pull.id
        try:
            linked_issues.append(pull_to_issue[pull.id])
        except:
            print "pull not in list"

    print "Length of issues " + str(len(linked_issues))

    # Start collection of text the dev likes and dislikes
    dev_corpus = {}
    for dev in cur_project.devs:
        print "adding dev"
        dev_corpus[dev.dev_id] = {}
        dev_corpus[dev.dev_id]["good"] = ""
        dev_corpus[dev.dev_id]["bad"] = ""

    # Order issues chronologically
    chron_issues = sorted(linked_issues, key=lambda x: x.created_at)
    print "sorted issues"

    # Count how many issues would have been predicted correctly by each 
    # technnique
    correct = []
    correct.append(0) # homebrew
    correct.append(0) # leven
    correct.append(0) # cosine
    correct.append(0) # stemmed normalized cosine
    correct.append(len(chron_issues))

    for issue in chron_issues:
        print issue.title
        cur_dev = issue_to_pull[issue.issue_id].dev_id
        debug += "================================================== <br>"
        debug += "cur dev: " + str(cur_dev) + "<br>"
        debug += "cur issue: " + str(issue.title) + "<br>"
        debug += "corpus = " + str(dev_corpus[cur_dev]) + "<br>" + "<br>"
        open_issues = get_other_issues_open(issue, cur_project.issues)

        best_guesses = []
        worst_guesses = []
        avg_guesses = []
        for open_issue in open_issues:
            cur_text = (open_issue.desc + " " + open_issue.title).encode('utf-8').strip()

            csv += str(issue.issue_id) + ", "
            # Compute good similarity
            corpus = str(dev_corpus[cur_dev]["good"])
            homebrew_good = ts.homebrew_nlp(cur_text, corpus) * 100
            leven_good = ts.levenshtein(cur_text, corpus) * 100
            cosine_good = ts.cosine_test(cur_text, corpus) * 100
            stem_cosine_good = ts.stem_trimmed_cosine(cur_text, corpus) * 100
            csv += str(open_issue.issue_id) + ", "
            csv += str(homebrew_good) + ", " + str(leven_good) + ", " + str(cosine_good) + ", " + str(stem_cosine_good) + ", "
            if int(open_issue.issue_id) == int(issue.issue_id):
                csv += "1"
            else:
                csv += "0"
            csv += "<br>"
            best_guesses.append((homebrew_good, leven_good, cosine_good, stem_cosine_good, open_issue))
            
            # Compute bad similarity
            corpus = str(dev_corpus[cur_dev]["bad"])
            homebrew_bad = ts.homebrew_nlp(cur_text, corpus) * 100
            leven_bad = ts.levenshtein(cur_text, corpus) * 100
            cosine_bad = ts.cosine_test(cur_text, corpus) * 100
            stem_cosine_bad = ts.stem_trimmed_cosine(cur_text, corpus) * 100
            worst_guesses.append((homebrew_bad, leven_bad, cosine_bad, stem_cosine_bad, open_issue))
    
            avg_guesses.append((homebrew_good - homebrew_bad, 
                             leven_good - leven_bad,
                             cosine_good - cosine_bad, open_issue))
            dev_corpus[cur_dev]["bad"] += cur_text

        dev_corpus[cur_dev]["good"] += issue.desc + " " + issue.title
        csv += "<br>"
            
        if len(best_guesses) > 0:
            best_guess = sorted(best_guesses, key=lambda x: x[0], reverse=True)
            if best_guess[0][-1].issue_id == issue.issue_id:
                correct[0] += 1

            best_guess = sorted(best_guesses, key=lambda x: x[1], reverse=True)
            if best_guess[0][-1].issue_id == issue.issue_id:
                correct[1] += 1

            best_guess = sorted(best_guesses, key=lambda x: x[2], reverse=True)
            if best_guess[0][-1].issue_id == issue.issue_id:
                correct[2] += 1

            best_guess = sorted(best_guesses, key=lambda x: x[3], reverse=True)
            if best_guess[0][-1].issue_id == issue.issue_id:
                correct[3] += 1


        worst_guess = sorted(worst_guesses, key=lambda x: x[0], reverse=True)
        avg_guess = sorted(avg_guesses, key=lambda x: x[0], reverse=True)

        debug += "Best guesses: <br>"
        for item in best_guess:
            debug += " ".join((str(item[0]), str(item[1]), str(item[2]), item[3].title)) + "<br>"
        debug += "<br>"

        debug += "worst guesses: <br>"
        for item in worst_guess:
            debug += " ".join((str(item[0]), str(item[1]), str(item[2]), item[3].title)) + "<br>"
        debug += "<br>"

        debug += "avg guesses: <br>"
        for item in avg_guess:
            debug += " ".join((str(item[0]), str(item[1]), str(item[2]), item[3].title)) + "<br>"
        debug += "<br>"

    return debug, correct, csv

def get_classid(project, classname):
    my_class = [x for x in project.classfiles if x.path == classname]
    return my_class[0].id

def get_other_issues_open(cur_issue, issue_list):
    open_issues = []
    for issue in issue_list:
        if issue.closed_at is not None and cur_issue.closed_at is not None:
            if issue.created_at <= cur_issue.closed_at and issue.created_at >= cur_issue.created_at:
                open_issues.append(issue)
        else:
            continue
    return open_issues

def find_most_similar(cur_req, past_reqs):
    max_similar = -1
    new_mapping = {}
    for req in past_reqs:
        percent_similar = homebrew_nlp(cur_req.desc, req.desc)
        if percent_similar > max_similar:
            max_similar = percent_similar
            new_mapping = req.class_affinity
    return new_mapping

def get_all_similar(cur_req, past_reqs):
    mapping = {}
    for req in past_reqs:
        combined_cur = cur_req.desc + " " + cur_req.title
        combined_past = req.desc + " " + req.title
        ts = TextualSimilarity()
        percent_similar_cosine = ts.cosine_test(combined_cur, combined_past) * 100
        percent_similar_leven = ts.levenshtein(combined_cur, combined_past) * 100
        percent_similar_homebrew = ts.homebrew_nlp(combined_cur, combined_past) * 100
        mapping[req.title] = []
        mapping[req.title].append(req.churn)
        mapping[req.title].append(percent_similar_cosine)
        mapping[req.title].append(percent_similar_leven)
        mapping[req.title].append(percent_similar_homebrew)
        mapping[req.title].append(round(req.churn * (percent_similar_leven + percent_similar_homebrew + percent_similar_cosine), 2))
    return mapping

def issue_from_id(id, project):
    for issue in project.issues:
        if int(id) == int(issue.issue_id):
            return issue

def dev_from_id(project, pull):
    print pull.user.id
    dev_list = [x for x in project.devs if x.dev_id == pull.user.id]
    if len(dev_list) > 0:
        return dev_list[0]
    else:
        return None

def modify_dev_affinity(project, pull, dev, is_positive):
    for changed_file in pull.get_files():
        print changed_file.filename
        classid = get_classid(project, changed_file.filename)
        print classid
        if classid not in dev.class_affinity.keys():
            dev.class_affinity[classid] = 0
        if is_positive:
            dev.class_affinity[classid] += 100
        elif not is_positive:
            dev.class_affinity[classid] += -20

def build_pull_to_issue_map(project):
    mapping = {}
    for pull in project.pulls:
        if "#" in pull.body:
            issue_num = pull.body.split("#")[1].split(" ")[0].strip()
            try:
                issue_num = int(issue_num)
                issue = [x for x in project.issues if x.issue_id == issue_num][0]
                mapping[pull.id] = issue
            except:
                continue
    return mapping

def build_issue_to_pull_map(project):
    mapping = {}
    for pull in project.pulls:
        if "#" in pull.body:
            issue_num = pull.body.split("#")[1].split(" ")[0].strip()
            try:
                issue_num = int(issue_num)
                mapping[issue_num] = pull
            except:
                continue
    return mapping

def get_other_issues_open(cur_issue, issue_list):
    open_issues = []
    for issue in issue_list:
        if issue.closed_at is not None and cur_issue.closed_at is not None:
            if issue.created_at <= cur_issue.closed_at and issue.created_at >= cur_issue.created_at:
                open_issues.append(issue)
        else:
            continue
    return open_issues

def build_corpus(cur_project):
    # Link pulls to issues
    result = ""
    pull_to_issue = build_pull_to_issue_map(cur_project)
    issue_to_pull = build_issue_to_pull_map(cur_project)
    linked_issues = []
    for pull in cur_project.pulls:
        if pull.id in pull_to_issue.keys():
            linked_issues.append(pull_to_issue[pull.id])

    # Start collection of text the dev likes
    dev_corpus = {}
    for dev in cur_project.devs:
        dev_corpus[dev.dev_id] = {}
        dev_corpus[dev.dev_id]["good"] = ""
        dev_corpus[dev.dev_id]["bad"] = ""

    # Order issues chronologically
    chron_issues = sorted(linked_issues, key=lambda x: x.created_at)
    for issue in chron_issues:
        cur_dev = issue_to_pull[issue.issue_id].dev_id
        dev_corpus[cur_dev]["good"] += issue.desc + " " + issue.title
        open_issues = get_other_issues_open(issue, cur_project.issues)
        for open_issue in open_issues:
            dev_corpus[cur_dev]["bad"] += open_issue.desc + " " + open_issue.title
    return dev_corpus
