from redmine import Redmine

class RedmineHelper:
    CUSTOM_FIELD_ID = {
        'component': 1,
        'reporter': 3,
        'version': 4
    }

    def __init__(self, url, developer_key):
        self.tracker = Redmine(url, key=developer_key)
        self.initialize_attributes()

    def initialize_attributes(self):
        self.issues = self.tracker.issue.all()
        # Caching versions will speed up the loop (from 98" to 12" with 252 issues)
        self._issues_versions()

    def version_component_matrix(self):
        matrix = {}
        for issue in self.issues:
            details = (str(issue.id), issue.url, issue.subject)
            version = self._issue_version(issue)
            component = self._issue_component(issue)

            if version not in matrix:
                matrix[version] = {}
            if component not in matrix[version]:
                matrix[version][component] = []

            matrix[version][component].append(details)

        return matrix

    def number_of_opened_issues(self):
        return len(self.issues)




    # Private methods
    def _issues_versions(self):
        self._versions = {}
        for issue in self.issues:
            version_id = self._issue_version_id(issue)
            if version_id not in self._versions:
                self._versions[version_id] = self.tracker.version.get(version_id).name




    # Getting single issue attributes (avoiding a "Issue" class)
    def _issue_version_id(self, issue):
        return issue.custom_fields.get(self.CUSTOM_FIELD_ID['version']).value

    def _issue_version(self, issue):
        version_id = issue.custom_fields.get(self.CUSTOM_FIELD_ID['version']).value
        if version_id not in self._versions:
            version = 'Unknown'
        else:
            version = self._versions[version_id]

        return version

    def _issue_component(self, issue):
        component = issue.custom_fields.get(self.CUSTOM_FIELD_ID['component']).value
        if not component:
            component = "none"

        return component

# FIXME: only for development
from configuration import ConfigurationParser
print "Reading configuration from file"
configuration = ConfigurationParser('dashboard.conf')
url, key = configuration.public_tracker_credentials()

print "Gathering ticket information"
public_tracker = RedmineHelper(url, key)
print "Version/component matrix:\n" + str(public_tracker.version_component_matrix())
print "Number of opened issues: " + str(public_tracker.number_of_opened_issues())
