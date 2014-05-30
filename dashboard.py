#!/usr/bin/python


from flask import Flask, render_template

from configuration import ConfigurationParser
from jenkins_parser import JenkinsHelper

# Getting configuration file information
configuration = ConfigurationParser()

# Getting jenkins information
zentyal_jenkins = JenkinsHelper(configuration)
jobs = zentyal_jenkins.get_jobs()
components = zentyal_jenkins.get_components()

app = Flask(__name__)

@app.route("/")
def stats():
    return render_template('stats.html', jobs=jobs, components=components)

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
