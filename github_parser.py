import requests

class GitHubHelper:
    fields = ('html_url', 'number', 'merge_commit_sha', 'assignee', 'title', 'body', 'created_at', 'state')

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_sufix = '?client_id=' + client_id + '&client_secret=' + client_secret

    def pull_requests(self, organization, repository):
        api_url = 'https://api.github.com/repos/' + organization + '/' + repository + '/pulls' + self.auth_sufix
        response = requests.get(api_url).json

        self.pull_requests = {}
        for pull_request in response:
            pull_request_dict = self.parse_initial_fields(pull_request)
            pull_request_dict['base_branch'] = self.merge_branch(pull_request)
            statuses, active = self.statuses(pull_request)
            pull_request_dict['statuses'] = statuses
            pull_request_dict['active'] = active
            pull_request_dict['user'] = self.parse_user_info(pull_request)
            pull_request_dict['branch'] = self.parse_branch_name(pull_request)
            pull_request_dict['build_state'] = self.last_build_state(pull_request_dict)

            pr_id = pull_request['number']
            self.pull_requests[pr_id] = pull_request_dict

        return self.pull_requests

    def base_branchs(self):
        self.branchs = []
        if self.pull_requests:
            for pr_id, pull_request in self.pull_requests.iteritems():
                if not pull_request['base_branch'] in self.branchs:
                    self.branchs.append(pull_request['base_branch'])

        return self.branchs

    # Helpers
    def parse_initial_fields(self, pull_request):
        pr_dict = {}
        for field in self.fields:
            if field in pull_request:
                pr_dict[field] = pull_request[field]
            else:
                pr_dict[field] = "None"

        return pr_dict

    def merge_branch(self, pull_request):
        if ('base' in pull_request) and ('ref' in pull_request['base']):
            return pull_request['base']['ref']
        else:
            return "None"

    def statuses(self, pull_request):
        statuses = []
        counter = 0
        active = False
        if 'statuses_url' in pull_request:
            response = requests.get(pull_request['statuses_url'] + self.auth_sufix).json
            for api_status in response:
                if not api_status['description'] == "Build finished.":
                    continue
                elif counter == 0 and api_status['state'] == "pending":
                    active = True

                status = {}
                status['url'] = api_status['target_url'] if 'target_url' in api_status else ""
                status['state'] = api_status['state'] if 'state' in api_status else ""

                statuses.append(status)
                counter += 1

        return (statuses, active)

    def parse_user_info(self, pull_request):
        if 'user' in pull_request:
            if 'login' in pull_request['user']:
                return pull_request['user']['login']

        return 'None'

    def parse_branch_name(self, pull_request):
        if 'head' in pull_request:
            if 'ref' in pull_request['head']:
                return pull_request['head']['ref']

        return 'None'

    def last_build_state(self, pull_request):
        result = 'build-none'

        if 'statuses' in pull_request:
            if len(pull_request['statuses']):
                result = 'build-' + pull_request['statuses'][0]['state']

        result += ' build-active ' if pull_request['active'] else ''

        return result
