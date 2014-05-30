from ConfigParser import SafeConfigParser

class ConfigurationParser:
    def __init__(self, filename):
        self.configuration = SafeConfigParser()
        self.configuration.read(filename)

    def jenkins_credentials(self):
        credentials = dict(self.configuration.items('auth'))

        return (credentials['url'], credentials['user'], credentials['pass'])

    def jenkins_jobs(self):
        main_configuration = dict(self.configuration.items('main'))
        jobs = main_configuration['jobs'].split()
        jobs_ids = main_configuration['jobs_ids'].split()

        return (jobs, jobs_ids)

    def jenkins_configuration_prefix(self):
        main_configuration = dict(self.configuration.items('main'))

        return main_configuration['conf_prefix']

    def jenkins_grouped_components(self):
        groups_configuration = dict(self.configuration.items('grouping'))

        return groups_configuration['key_sections'].split()

    def refresh_rate(self):
        refresh_rate = dict(self.configuration.items('configuration'))['refresh_rate']

        return int(refresh_rate) if refresh_rate else 60
