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
            pull_request_dict['merge_branch'] = self.merge_branch(pull_request)
            pull_request_dict['statuses'] = self.statuses(pull_request)

            pr_id = pull_request['number']
            self.pull_requests[pr_id] = pull_request_dict

        return self.pull_requests


    # Helpers
    def parse_initial_fields(self, pull_request):
        pr_dict = {}
        for field in self.fields:
            if field in pull_request:
                pr_dict[field] = pull_request[field]
            else:
                pr_dict[field] = ""

        return pr_dict

    def merge_branch(self, pull_request):
        if ('base' in pull_request) and ('ref' in pull_request['base']):
            return pull_request['base']['ref']
        else:
            return "None"

    def statuses(self, pull_request):
        statuses = []
        if 'statuses_url' in pull_request:
            response = requests.get(pull_request['statuses_url']).json
            for api_status in response:
                status = {}
                status['url'] = api_status['target_url'] if 'target_url' in api_status else ""
                status['state'] = api_status['state'] if 'state' in api_status else ""

                statuses.append(status)

        return statuses
