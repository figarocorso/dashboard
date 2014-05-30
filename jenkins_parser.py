from jenkins import Jenkins
import collections

class JenkinsHelper:
    def __init__(self, configuration):
        self.configuration = configuration
        self.configuration_prefix = configuration.jenkins_configuration_prefix()
        self.grouped_components = configuration.jenkins_grouped_components()

        self.jenkins = self.connect_to_jenkins()
        self.build_components_jobs_matrix()

    def initial_jobs_info(self):
        wanted_jobs, wanted_ids = self.configuration.jenkins_jobs()
        jobs = self.wanted_jobs(wanted_jobs)
        return self.add_human_name_to_job(jobs, wanted_ids)

    def wanted_jobs(self, wanted_jobs):
        jobs = self.jenkins.get_jobs()

        return [ job for job  in jobs if job['name'] in wanted_jobs ]

    def add_human_name_to_job(self, jobs, wanted_jobs_ids):
        for i in range(len(jobs)):
            jobs[i]['short_name'] = wanted_jobs_ids[i]

        return jobs


    def build_components_jobs_matrix(self):
        self.jobs = self.initial_jobs_info()

        self.components = {}
        for job in self.jobs:
            groups = {}
            job_raw_components = self.jenkins.get_job_info(job['name'])["activeConfigurations"]

            job['components'] = {}
            for raw_component in job_raw_components:
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
            # Add groups to job components
            for name, group in groups.iteritems():
                job['components'][name] = group
                self.components[name] = {}
                self.components[name]['name'] = group['name']
                self.components[name]['global_class'] = 'group'
                self.components[name]['type'] = 'group';


        # Sort components to show them properly
        self.components = collections.OrderedDict(sorted(self.components.items(), key=lambda x: self.sorting_modification(x)))

    # Getters
    def get_jobs(self):
        return self.jobs

    def get_components(self):
        return self.components

# Helper methods
    def connect_to_jenkins(self):
        url, username, password = self.configuration.jenkins_credentials()

        return Jenkins(url, username, password)


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

