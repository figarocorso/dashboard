from collections import OrderedDict

import jenkinsapi.jenkins
from jenkins import Jenkins

class JenkinsHelper:
    def __init__(self, url, username, password, key, configuration):
        self.configuration = configuration
        self.configuration_prefix = configuration.jenkins_configuration_prefix()
        self.grouped_components = configuration.jenkins_grouped_components()
        self.pullrequest_job = configuration.pullrequest_job()

        self.jenkins_configurations = Jenkins(url, username, password)
        self.build_components_jobs_matrix()
        self.sort_components()

        self.jenkins_builds = jenkinsapi.jenkins.Jenkins(url, username, password)
        job = self.jenkins_builds.get_job(self.pullrequest_job)

        self.pullrequest_builds = {}
        for build_id in job.get_build_ids():
            build = job[build_id]
            self.pullrequest_builds[build.buildno] = {}
            self.pullrequest_builds[build.buildno]['status'] = build.get_status()
            self.pullrequest_builds[build.buildno]['url'] = build.baseurl
            self.pullrequest_builds[build.buildno]['name'] = build.name
            self.pullrequest_builds[build.buildno]['revision'] = build.get_revision_branch()[0]['SHA1']

# Getters
    def get_jobs(self):
        return self.jobs

    def get_components(self):
        return self.components

# Helper methods
    def initial_jobs_info(self):
        wanted_jobs, wanted_ids = self.configuration.jenkins_jobs()
        jobs = self.wanted_jobs(wanted_jobs)
        return self.add_human_name_to_job(jobs, wanted_ids)

    def sort_components(self):
        self.components = OrderedDict(sorted(self.components.items(), key=lambda x: self.sorting_modification(x)))

    def build_components_jobs_matrix(self):
        self.jobs = self.initial_jobs_info()

        self.components = {}
        for job in self.jobs:
            groups = {}
            job_raw_components = self.jenkins_configurations.get_job_info(job['name'])["activeConfigurations"]

            job['components'] = {}
            for raw_component in job_raw_components:
                self.process_component(raw_component, job, groups)

            for name, group in groups.iteritems():
                job['components'][name] = group
                self.add_group_to_components(name, group)

    def add_group_to_components(self, name, group):
        self.components[name] = {}
        self.components[name]['name'] = group['name']
        self.components[name]['global_class'] = 'group'
        self.components[name]['type'] = 'group';

    def process_component(self, raw_component, job, groups):
        name = raw_component['name'].replace(self.configuration_prefix, '')

        if name not in self.components:
            self.components[name] = {}
            self.components[name]['name'] = name

        job['components'][name] = {};
        job['components'][name]['name'] = name;
        job['components'][name]['color'] = raw_component['color']
        job['components'][name]['href'] = raw_component['url']

        # Manage grouped components
        grouped_component = self.has_to_be_grouped(name, self.grouped_components)
        if grouped_component:
            self.components[name]['global_class'] = grouped_component + ' hide grouped'

            # Create component group entry
            group_name = grouped_component + '_grouped'
            if not group_name in groups:
                groups[group_name] = {'name': grouped_component, 'color': ''}

            groups[group_name]['color'] = self.logical_color_conjunction(
                                                        groups[group_name]['color'],
                                                        raw_component['color'])

# Second level helper methods
    def wanted_jobs(self, wanted_jobs):
        jobs = self.jenkins_configurations.get_jobs()

        return [ job for job  in jobs if job['name'] in wanted_jobs ]

    def add_human_name_to_job(self, jobs, wanted_jobs_ids):
        for i in range(len(jobs)):
            jobs[i]['short_name'] = wanted_jobs_ids[i]

        return jobs


    def has_to_be_grouped(self, name, grouped_configuration):
        for keyword in grouped_configuration:
            if name.find(keyword) == 0:
                return keyword

        return False


    def logical_color_conjunction(self, color1, color2):
        if (color1 == 'red' or color2 == 'red'):
            return 'red'
        if (color1 == 'yellow' or color2 == 'yellow'):
            return 'yellow'
        if (color1 == 'blue' or color2 == 'blue'):
            return 'blue'

        return 'white'

    def sorting_modification(self, value):
        if ('type' in value[1]) and (value[1]['type'] == 'group'):
            return value[1]['name']

        return value[0] + "_"

