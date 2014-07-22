import collections

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
        self._issues_status_counting()

    def component_version_matrix(self):
        matrix = {}
        for issue in self.issues:
            details = self._issue_details(issue)

            component = self._issue_component(issue)
            version = self._issue_version(issue)
            status = issue.status.name

            if component not in matrix:
                matrix[component] = {}
            if version not in matrix[component]:
                matrix[component][version] = {}
            if status not in matrix[component][version]:
                matrix[component][version][status] = []

            if (status == 'New' or status == 'Accepted'):
                if 'open' not in matrix[component][version]:
                    matrix[component][version]['open'] = []

                details['status'] = status
                matrix[component][version]['open'].append(details)

                if 'number_issues_open' in matrix[component][version]:
                    matrix[component][version]['number_issues_open'] += 1
                else:
                    matrix[component][version]['number_issues_open'] = 1

            matrix[component][version][status].append(details)

        return collections.OrderedDict(sorted(matrix.items()))

    def versions(self):
        versions = []

        for version_id, version in self._versions.iteritems():
            versions.append(version)

        return sorted(versions)

    def issues_status_stats(self):
        return self._status_count

    def number_of_opened_issues(self):
        return self._status_count['New'] + self._status_count['Accepted']

    def assigned_issues_by_developer(self):
        developers_matrix = {}
        for issue in self.issues:
            if hasattr(issue, 'assigned_to'):
                assignee = issue.assigned_to.name
                if assignee not in developers_matrix:
                    developers_matrix[assignee] = []

                developers_matrix[assignee].append(self._issue_details(issue))

        return developers_matrix

    # Private methods
    def _issues_versions(self):
        self._versions = {}
        for issue in self.issues:
            version_id = self._issue_version_id(issue)
            if version_id not in self._versions:
                self._versions[version_id] = self.tracker.version.get(version_id).name

    def _issues_status_counting(self):
        self._status = {}
        self._status_count = {}

        for issue in self.issues:
            status_name = issue.status.name
            if status_name not in self._status:
                self._status[status_name] = []

            self._status[status_name].append(self._issue_details(issue))

        for status_name in self._status:
            self._status_count[status_name] = len(self._status[status_name])

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

    def _issue_details(self, issue):
        return {'id': str(issue.id), 'url': issue.url, 'subject': issue.subject}
