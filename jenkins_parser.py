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
        self.jenkins_builds = jenkinsapi.jenkins.Jenkins(url, username, password)

# Getters
    def get_jobs(self):
        return self.processed_jobs

    def get_versions(self):
        versions = []
        for name, version in self.wanted_jobs.iteritems():
            versions.append(version)

        return sorted(versions)

    def get_pull_request_builds(self):
        job = self.jenkins_builds.get_job(self.pullrequest_job)

        self.pullrequest_builds = {}
        for build_id in job.get_build_ids():
            build = job[build_id]
            self.pullrequest_builds[build.buildno] = {}
            self.pullrequest_builds[build.buildno]['status'] = build.get_status()
            self.pullrequest_builds[build.buildno]['url'] = build.baseurl
            self.pullrequest_builds[build.buildno]['name'] = build.name

            revision = build.get_revision_branch()[0]
            self.pullrequest_builds[build.buildno]['revision'] = revision['SHA1']
            self.pullrequest_builds[build.buildno]['revision_name'] = revision['name']

        return self.pullrequest_builds

# Helper methods
    def build_components_jobs_matrix(self):
        self.wanted_jobs = self.get_name_version_dictionary()
        self.backlist_keywords = self.configuration.jenkins_blacklist()
        (jobs, jobs_sets) = self.obtain_jobs_to_parse()
        self.jobs = self.get_jobs_details(jobs, jobs_sets)
        self.processed_jobs = self.process_jobs()
        self.sort_components()

    def get_name_version_dictionary(self):
        wanted_jobs, wanted_ids = self.configuration.jenkins_jobs()

        # build a dictionary with keywords name-version
        self.wanted_jobs = {}
        for i in range(len(wanted_jobs)):
            self.wanted_jobs[wanted_jobs[i]] = wanted_ids[i]

        return OrderedDict(sorted(self.wanted_jobs.iteritems(), key=lambda x: len(x[0]), reverse=True))

    def obtain_jobs_to_parse(self):
        jobs = self.jenkins_configurations.get_jobs()
        jobs_sets = []
        single_jobs = []
        for job in jobs:
            if self.job_is_blacklisted(job):
                continue

            for job_prefix, version in self.wanted_jobs.iteritems():
                if '/' + job_prefix.lower()  + '/' in  job['url'].lower():
                    job['version'] = version
                    jobs_sets.append(job)
                    break
                elif job_prefix.lower() in job['url'].lower():
                    job['version'] = version
                    single_jobs.append(job)
                    break

        return (single_jobs, jobs_sets)

    def job_is_blacklisted(self, job):
        for keyword in self.backlist_keywords:
            if not job['url'].lower().find(keyword.lower()) == -1:
                return True

        return False

    def get_jobs_details(self, jobs, jobs_sets):
        jobs_details = jobs
        for jobs_set in jobs_sets:
            jobs_set_jobs = self.jenkins_configurations.get_job_info(jobs_set['name'])["activeConfigurations"]
            for job in jobs_set_jobs:
                job['version'] = jobs_set['version']
            jobs_details += jobs_set_jobs

        return jobs_details

    def process_jobs(self):
        processed_jobs = {}
        groups = {}
        for job in self.jobs:
            self.process_job(job, groups)
            if not job['name'] in processed_jobs:
                processed_jobs[job['name']] = {}

            processed_jobs[job['name']][job['version']] = job
            processed_jobs[job['name']]['name'] = job['name']
            if 'global_class' in job:
                processed_jobs[job['name']]['global_class'] = job['global_class']

        for name, group in groups.iteritems():
            self.add_group_to_components(name, group, processed_jobs)

        return processed_jobs

    def sort_components(self):
        self.processed_jobs = OrderedDict(sorted(self.processed_jobs.items(),
                                                key=lambda x: self.sorting_modification(x)))


    def add_group_to_components(self, name, group, processed_jobs):
        processed_jobs[name] = group
        processed_jobs[name]['global_class'] = 'group'
        processed_jobs[name]['type'] = 'group'
        processed_jobs[name]['name'] = group['name']

    def process_job(self, job, groups):
        job['name'] = job['name'].replace(self.configuration_prefix, '')
        job['name'] = job['name'].lower()
        for name, version in self.wanted_jobs.iteritems():
            job['name'] = job['name'].replace(name.lower() + '_', '')
            job['name'] = job['name'].replace(name.lower(), '')

        # Manage grouped components
        grouped_component = self.has_to_be_grouped(job['name'], self.grouped_components)
        if grouped_component:
            job['global_class'] = grouped_component + ' hide grouped'

            # Create component group entry
            group_name = grouped_component + '_grouped'
            if not group_name in groups:
                groups[group_name] = {}
                groups[group_name]['name'] = grouped_component

            if not job['version'] in groups[group_name]:
                groups[group_name][job['version']] = {'name': grouped_component,
                                                            'global_class': 'group',
                                                            'color': ''}

            groups[group_name][job['version']]['color'] = self.logical_color_conjunction(
                                                        groups[group_name][job['version']]['color'],
                                                        job['color'])

# Second level helper methods
    def has_to_be_grouped(self, name, grouped_configuration):
        for keyword in grouped_configuration:
            if not name.lower().find(keyword.lower()) == -1:
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

        return value[0] + '_'

