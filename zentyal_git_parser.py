import re
from subprocess import check_output
from os import system, chdir, getcwd

class ZentyalGitHelper:
    def __init__(self, repo_path, pull_requests):
        self.repo_path = repo_path
        self.pull_requests = pull_requests
        self.pending_packages = {}
        self.initialize_pr_data()
        self.initialize_packages()

    def initialize_pr_data(self):
        pr_data = {}
        for number, pr in self.pull_requests.iteritems():
            branch = pr['base_branch']
            if not pr_data.has_key(branch):
                pr_data[branch] = {}

            modules = self.get_modified_modules_in_pull_request(number)
            for module in modules:
                if not pr_data[branch].has_key(module):
                    pr_data[branch][module] = []
                pr_data[branch][module].append(number)

        self.pr_data = pr_data

    def initialize_packages(self):
        cwd = getcwd()
        main_path = self.repo_path + "/main"
        chdir(main_path)
        for branch in ('master', '3.2'):
            system("git checkout " + branch)
            # FIXME: this is commented while developing
            #system("git pull")
            branch = "zentyal/" + branch
            self.pending_packages[branch] = []
            packages = filter(None, check_output("ls").split('\n'))
            for package in packages:
                changelog = main_path + '/' + package + '/ChangeLog'
                changes = ''
                with open(changelog) as f:
                    lines = f.readlines()
                    if lines[0].startswith("HEAD"):
                        del lines[0]
                        for line in lines:
                            if re.search("^\s", line):
                                changes += line
                            else:
                                break
                pull_requests = []
                if self.pr_data[branch].has_key(package):
                    pull_requests = self.pr_data[branch][package]
                if changes or pull_requests:
                    self.pending_packages[branch].append({ 'name': package, 'changes': changes, 'prs' : pull_requests })
        chdir(cwd)

    def get_pending_packages(self):
        return self.pending_packages

    # FIXME: this should probably be moved to the GitHub helper
    def get_modified_modules_in_pull_request(self, pr_id):
        # FIXME use requests module instead of curl
        output = check_output('curl https://github.com/Zentyal/zentyal/pull/' + str(pr_id) + '.diff 2>/dev/null | grep "/ChangeLog$" |cut -d/ -f3 | sort | uniq', shell=True)
        return filter(None, output.split('\n'))
