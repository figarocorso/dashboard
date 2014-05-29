#!/usr/bin/python

import jenkins
import collections

from flask import Flask, render_template

from configuration import ConfigurationParser

def has_to_be_grouped(name, grouped_configuration):
    for keyword in grouped_configuration:
        if name.find(keyword) == 0:
            return keyword

    return False

def logical_color_conjunction(color1, color2):
    if (color1 == 'red' or color2 == 'red'):
        return 'red'
    if (color1 == 'yellow' or color2 == 'yellow'):
        return 'yellow'
    if (color1 == 'blue' or color2 == 'blue'):
        return 'blue'

    return 'white'

def sorting_modification(value):
    if ('type' in value[1]) and (value[1]['type'] == 'group'):
        return value[1]['name']

    return value[0] + "_"

#TODO Monolithic!!

# Load configuration file parameters
configuration = ConfigurationParser()
url, username, password = jenkins_configuration = configuration.jenkins_credentials()
wanted_jobs, wanted_jobs_ids = configuration.jenkins_jobs()
configuration_prefix = configuration.jenkins_configuration_prefix()
grouped_components = configuration.jenkins_grouped_components()

# Stablishing connection
jenkins = jenkins.Jenkins(url, username, password)

# Getting wanted jobs
jobs = jenkins.get_jobs()
jobs = [ job for job  in jobs if job['name'] in wanted_jobs ]
for i in range(len(jobs)):
    jobs[i]['short_name'] = wanted_jobs_ids[i]

# Getting component configurations from jobs
components = {}
for job in jobs:
    groups = {}
    job_raw_components = jenkins.get_job_info(job['name'])["activeConfigurations"]

    job['components'] = {}
    for raw_component in job_raw_components:
        name = raw_component['name'].replace(configuration_prefix, '')

        if name not in components:
            components[name] = {}
            components[name]['name'] = name

        job['components'][name] = {};
        job['components'][name]['name'] = name;
        job['components'][name]['color'] = raw_component['color']
        job['components'][name]['href'] = raw_component['url']

        # Manage grouped components
        grouped_component = has_to_be_grouped(name, grouped_components)
        if grouped_component:
            components[name]['global_class'] = grouped_component + ' hide grouped'

            # Create component group entry
            group_name = grouped_component + '_grouped'
            if not group_name in groups:
                groups[group_name] = {'name': grouped_component, 'color': ''}

            groups[group_name]['color'] = logical_color_conjunction(
                                                        groups[group_name]['color'],
                                                        raw_component['color'])
    # Add groups to job components
    for name, group in groups.iteritems():
        job['components'][name] = group
        components[name] = {}
        components[name]['name'] = group['name']
        components[name]['global_class'] = 'group'
        components[name]['type'] = 'group';


# Sort components to show them properly
components = collections.OrderedDict(sorted(components.items(), key=lambda x: sorting_modification(x)))

app = Flask(__name__)

@app.route("/")
def stats():
    return render_template('stats.html', jobs=jobs, components=components)

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
