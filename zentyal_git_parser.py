from subprocess import check_output
from os import system, chdir, getcwd

class ZentyalGitHelper:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.pending_packages = {}
        self.initialize_packages()

    def initialize_packages(self):
        cwd = getcwd()
        main_path = self.repo_path + "/main"
        chdir(main_path)
        for branch in ('master', '3.2'):
            self.pending_packages[branch] = []
            system("git checkout " + branch)
            # FIXME: this is commented while developing
            #system("git pull")
            packages = check_output("ls").split('\n')
            for package in packages:
                if not package:
                    continue
                changelog = main_path + '/' + package + '/ChangeLog'
                with open(changelog) as f:
                    lines = f.readlines()
                    if not lines[0].startswith("HEAD"):
                        continue
                self.pending_packages[branch].append(package)
        chdir(cwd)

    def get_pending_packages(self):
        return self.pending_packages
