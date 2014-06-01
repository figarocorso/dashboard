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
TRACKER_URL  = 'https://tracker.zentyal.org'
TRACKER_KEY  = ''

# binding
public_tracker = Redmine(TRACKER_URL, key=TRACKER_KEY)

# issue {attachments author changesets children created_on custom_fields description done_ratio
#       id journals priority project relations start_date status subject time_entries tracker updated_on watchers }
issues = public_tracker.issue.all()

datas = {}
versions = {}
statuses = []
assigned = {}
for issue in issues:
    issue_details = (str(issue.id),issue.url)

    if issue.status.name not in statuses:
        statuses.append(issue.status.name)

    if hasattr(issue, 'assigned_to'):
        if issue.assigned_to.name not in assigned:
            assigned[issue.assigned_to.name] = []
        assigned[issue.assigned_to.name].append(issue_details)

    component = issue.custom_fields.get(CUSTOM_FIELD_ID['component']).value
    version_id = issue.custom_fields.get(CUSTOM_FIELD_ID['version']).value
    # Speeding up the loop (from 98" to 12" with 252 issues)
    if version_id not in versions:
        version = public_tracker.version.get(version_id).name
        versions[version_id] = version
    else:
        version = versions[version_id]

    if not component:
        component = "none"
    if (not version) or (version == 'Unknown'):
        version = "none"

    if version not in datas:
        datas[version] = {}
    if component not in datas[version]:
        datas[version][component] = []

    datas[version][component].append(issue_details)

print "Total number of issues: " + str(len(issues))
print(statuses)
for version, components in datas.iteritems():
    for component in components:
        print version + " - " + component + ": " + str(len(datas[version][component]))
