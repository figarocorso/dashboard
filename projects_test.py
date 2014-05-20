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
tracker = Redmine(TRACKER_URL, key=TRACKER_KEY)

# issue {attachments author changesets children created_on custom_fields description done_ratio
#       id journals priority project relations start_date status subject time_entries tracker updated_on watchers }
issues = tracker.issue.all()
datas = {}

for issue in issues:
  comp = issue.custom_fields.get(CUSTOM_FIELD_ID['component']).value
  if comp not in datas:
    datas[comp] = []
  datas[comp].append((str(issue.id),issue.url)) 
  
print "Total number of issues: " + str(len(issues))
for data in datas:
  print data + ": " + repr([ x[0] for x in datas[data] ])
