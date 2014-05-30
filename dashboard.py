#!/usr/bin/python

from datetime import datetime

from flask import Flask, render_template

from configuration import ConfigurationParser
from jenkins_parser import JenkinsHelper

class ModulesInfo:
    def __init__(self):
        self.load_jenkins_info()

    @classmethod
    def load_jenkins_info(self):
        self.configuration = ConfigurationParser('dashboard.conf')
        self.REFRESH_RATE = self.configuration.refresh_rate()

        try:
            time_difference = (datetime.now() - self.last_data_loaded).seconds
        except AttributeError:
            time_difference = self.REFRESH_RATE + 1

        if (time_difference > self.REFRESH_RATE):
            self.last_data_loaded = datetime.now()

            zentyal_jenkins = JenkinsHelper(self.configuration)
            self.jobs = zentyal_jenkins.get_jobs()
            self.components = zentyal_jenkins.get_components()


app = Flask(__name__)

@app.route("/")
def dashboard():
    modules_info = ModulesInfo()
    jobs = modules_info.jobs
    components = modules_info.components

    return render_template('dashboard.html', jobs=jobs, components=components)

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
