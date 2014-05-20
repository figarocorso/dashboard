#!/usr/bin/python
from redmine import Redmine

CUSTOM_FIELD_ID = {
    'component': 1,
    'reporter': 3,
    'version': 4
}

def get_custom_field(issue, field_name):
    for field in issue.custom_fields:
        if field.name == field_name:
            return field.value

    return ''

# SCRIPT BEGINNING

# constants
INTERNAL_URL = 'https://projects.zentyal.com'
INTERNAL_KEY = ''

TRACKER_URL = 'https://tracker.zentyal.org'
TRACKER_KEY = ''

# binding
#internal = Redmine(INTERNAL_URL, key=INTERNAL_KEY)
tracker = Redmine(TRACKER_URL, key=TRACKER_KEY)

zentyal_public = tracker.project.get('zentyal')

# issue {attachments author changesets children created_on custom_fields description done_ratio
#       id journals priority project relations start_date status subject time_entries tracker updated_on watchers }
issues = tracker.issue.all()
issue = issues[0]
print "Total number of issues: " + str(len(issues))
print "Issue ID: " + str(issue.id)

issues = tracker.issue.filter(cf_1='monitor')
issue = issues[0]
print "Total number of issues: " + str(len(issues))
print "Issue ID: " + str(issue.id)

#issue = zentyal_public.issues.get('698')
#print "The number of monitor issues is: " + str(issues.total_count)

#print "The id is: " + str(issue.id)

# status { New, Accepted, Feedback, Rejected, Duplicated, Fixed }
#print "The status is: " + str(issue.status)

# Getting component
#print "The component is: " + get_custom_field(issue, "Component")

# Product version
#print "The version is: " + tracker.version.get(issue.custom_fields.get(4).value).name
