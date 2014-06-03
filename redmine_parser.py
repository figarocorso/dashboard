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
        self._versions = {}


    def number_of_opened_issues(self):
        return len(self.issues)

# FIXME: only for development
from configuration import ConfigurationParser
print "Reading configuration from file"
configuration = ConfigurationParser('dashboard.conf')
url, key = configuration.public_tracker_credentials()

print "Gathering ticket information"
public_tracker = RedmineHelper(url, key)
print "Number of opened issues: " + str(public_tracker.number_of_opened_issues())
