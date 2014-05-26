#!/usr/bin/python

import collections
from ConfigParser import SafeConfigParser

from flask import Flask, render_template

import jenkins

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


#TODO Monolithic!!

# Load configuration file parameters
configuration = SafeConfigParser()
configuration.read( 'dashboard.conf' )
jenkins_configuration = dict(configuration.items('auth'))
main_configuration = dict(configuration.items('main'))
groups_configuration = dict(configuration.items('grouping'))

wanted_jobs = main_configuration['jobs'].split()
wanted_jobs_ids = main_configuration['jobs_ids'].split()

grouped_components = groups_configuration['key_sections'].split()

# Stablishing connection
jenkins = jenkins.Jenkins(
            jenkins_configuration['url'],
            jenkins_configuration['user'],
            jenkins_configuration['pass'])

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
        name = raw_component['name'].replace(main_configuration['conf_prefix'],'')

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
                groups[group_name] = {'name': grouped_component, 'href': '#', 'color': ''}

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

    # Sort job components to show them properly
    job['components'] = collections.OrderedDict(sorted(job['components'].items()))

components = collections.OrderedDict(sorted(components.items()))

#for name, component in jobs[2]['components'].iteritems():
#    print name
#    print component['color']
#for name, component in components.iteritems():
#    print name
#    print component


app = Flask(__name__)

@app.route("/")
def stats():
    return render_template('stats.html', jobs=jobs, components=components)

if __name__ == "__main__":
    app.run(debug=True)
