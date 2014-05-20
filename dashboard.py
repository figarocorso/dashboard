#!/usr/bin/python
#
from ConfigParser import SafeConfigParser
from flask import Flask, render_template
import jenkins

conf = SafeConfigParser()
conf.read( 'dashboard.conf' )

url  = conf.get( 'main', 'url'  )
user = conf.get( 'auth', 'user' )
pwd  = conf.get( 'auth', 'pass' )
sfx  = conf.get( 'main', 'job_suffix'  )
pfx  = conf.get( 'main', 'conf_prefix' )

j = jenkins.Jenkins(url, user, pwd)

jerbs = j.get_jobs()
jerbs = [ x for x in jerbs if x['name'].endswith(sfx) ]
confs = []

for jerb in jerbs:
  jerb['sname'] = jerb['name'][:(len(sfx)*-1)]
  jerb['confs'] = {}
  jerb_confs = j.get_job_info(jerb['name'])["activeConfigurations"]
  
  for conf in jerb_confs:
    sname = conf['name'][len(pfx):]
    if sname not in confs:
      confs.append( sname )
    conf['sname'] = sname
    jerb['confs'][sname] = conf

confs.sort()

app = Flask(__name__)

@app.route("/")
def stats():
  return render_template('stats.html', jerbs=jerbs, confs=confs)

if __name__ == "__main__":
    app.run()
