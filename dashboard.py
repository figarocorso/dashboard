#!/usr/bin/python

from datetime import datetime

from flask import Flask, render_template

from configuration import ConfigurationParser
from jenkins_parser import JenkinsHelper
from redmine_parser import RedmineHelper

class ModulesInfo:
    @classmethod
    def cached_data_is_valid(self, refresh_rate, module):
        timestamp = 'last_' + module + '_loaded'
        if hasattr(self, timestamp):
            time_difference = (datetime.now() - getattr(self, timestamp)).seconds
        else:
            time_difference = refresh_rate + 1

        return time_difference < refresh_rate

    @classmethod
    def load_jenkins_info(self):
        configuration = ConfigurationParser('dashboard.conf')
        if not self.cached_data_is_valid(configuration.refresh_rate(), 'jenkins'):
            self.last_jenkins_loaded = datetime.now()
            zentyal_jenkins = JenkinsHelper(configuration)
            self.jobs = zentyal_jenkins.get_jobs()
            self.components = zentyal_jenkins.get_components()


    @classmethod
    def load_public_tracker_info(self):
        configuration = ConfigurationParser('dashboard.conf')
        if not self.cached_data_is_valid(configuration.refresh_rate(), 'public_redmine'):
            self.last_public_redmine_loaded = datetime.now()
            url, key = configuration.public_tracker_credentials()
            public_tracker = RedmineHelper(url, key)


app = Flask(__name__)

@app.route("/")
def dashboard():
    modules_info = ModulesInfo()
    modules_info.load_jenkins_info()

    return render_template('dashboard.html',
                                jobs = modules_info.jobs,
                                components = modules_info.components
                          )

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
