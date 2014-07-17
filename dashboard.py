#!/usr/bin/python

from datetime import datetime
from threading import Timer

from flask import Flask, render_template

from configuration import ConfigurationParser
from jenkins_parser import JenkinsHelper
from redmine_parser import RedmineHelper
from github_parser import GitHubHelper

class ModulesInfo:
    @classmethod
    def auto_updater(self):
        configuration = ConfigurationParser('dashboard.conf')
        Timer(configuration.refresh_rate(), self.auto_updater).start()
        now = datetime.now()
        self.last_update = str(now.hour).zfill(2) + ":" + str(now.minute % 60).zfill(2)

        # Load jenkins info
        url, user, password, key = configuration.jenkins_credentials()
        zentyal_jenkins = JenkinsHelper(url, user, password, key, configuration)
        self.jobs = zentyal_jenkins.get_jobs()
        self.components = zentyal_jenkins.get_components()

        # Load public tracker info
        url, key = configuration.public_tracker_credentials()
        self.public_tracker = RedmineHelper(url, key)

        # Load github pull requests
        client_id, client_secret = configuration.github_credentials()
        self.github = GitHubHelper(client_id, client_secret)
        repositories = configuration.github_repositories()

        for repo in repositories:
            self.github.add_pull_requests(repo['organization'], repo['repository'])

        self.pullrequests = self.github.get_pull_requests()
        self.base_branchs = self.github.base_branchs()

# Load initial data
modules_info = ModulesInfo()
modules_info.auto_updater()

app = Flask(__name__)

@app.route("/")
def dashboard():
    modules_info = ModulesInfo()

    return render_template('dashboard.html',
                                update_date = modules_info.last_update,
                                jobs = modules_info.jobs,
                                components = modules_info.components
                          )

@app.route("/jenkins")
def jenkins():
    modules_info = ModulesInfo()

    return render_template('jenkins.html',
                                update_date = modules_info.last_update,
                                jobs = modules_info.jobs,
                                components = modules_info.components
                          )

@app.route("/public-tracker")
def public_tracker():
    modules_info = ModulesInfo()
    tracker = modules_info.public_tracker

    component_issues = tracker.component_version_matrix()
    issues_versions = tracker.versions()
    issues_status_count = tracker.issues_status_stats()
    developer_matrix = tracker.assigned_issues_by_developer()

    return render_template('public-tracker.html',
                                update_date = modules_info.last_update,
                                components = component_issues,
                                versions = issues_versions,
                                issues_stats = issues_status_count,
                                developers = developer_matrix
                            )

@app.route("/pulls")
def pull_requests():
    modules_info = ModulesInfo()

    return render_template('pull-requests.html',
                                update_date = modules_info.last_update,
                                pulls = modules_info.pullrequests,
                                base_branchs = modules_info.base_branchs
                          )

if __name__ == "__main__":
    app.run(host='0.0.0.0')
