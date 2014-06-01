#!/usr/bin/python

from datetime import datetime

from flask import Flask, render_template

from configuration import ConfigurationParser
from jenkins_parser import JenkinsHelper

class ModulesInfo:
    def __init__(self):
        if not self.cached_data_is_valid():
            self.last_data_loaded = datetime.now()
            self.load_jenkins_info()

    @classmethod
    def cached_data_is_valid(self):
        self.configuration = ConfigurationParser('dashboard.conf')
        self.REFRESH_RATE = self.configuration.refresh_rate()
        try:
            time_difference = (datetime.now() - self.last_data_loaded).seconds
        except AttributeError:
            time_difference = self.REFRESH_RATE + 1
            self.last_data_loaded = datetime.now()

        return time_difference < self.REFRESH_RATE

    @classmethod
    def load_jenkins_info(self):
        zentyal_jenkins = JenkinsHelper(self.configuration)
        self.jobs = zentyal_jenkins.get_jobs()
        self.components = zentyal_jenkins.get_components()


app = Flask(__name__)

@app.route("/")
def dashboard():
    modules_info = ModulesInfo()

    return render_template('dashboard.html',
                                jobs = modules_info.jobs,
                                components = modules_info.components
                          )

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
