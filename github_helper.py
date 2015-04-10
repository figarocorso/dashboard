import requests
import json

class GitHubParser:
    fields = ('html_url', 'number', 'merge_commit_sha', 'assignee', 'title', 'body', 'created_at', 'state')

    def __init__(self):
        self.pull_requests = {}

    def add_pull_requests(self, pull_requests_data, organization, repository):
        pull_requests = {}
        for status, pull_request in pull_requests_data:
            pull_request_dict = self._parse_initial_fields(pull_request)
            full_base_branch = pull_request['head']['repo']['name'] + '/' + self._merge_branch(pull_request)
            pull_request_dict['base_branch'] = full_base_branch
            statuses, active = self._statuses(status)
            pull_request_dict['statuses'] = statuses
            pull_request_dict['active'] = active
            pull_request_dict['user'] = self._parse_user_info(pull_request)
            pull_request_dict['branch'] = self._parse_branch_name(pull_request)
            pull_request_dict['build_state'] = self._build_state(pull_request_dict)
            pull_request_dict['organization'] = organization
            pull_request_dict['repository'] = repository

            pr_id = pull_request['number']
            pull_requests[pr_id] = pull_request_dict

        # Append new pull requests to the existing ones
        self.pull_requests.update(pull_requests)

    def get_pull_requests(self):
        return self.pull_requests

    def base_branchs(self):
        self.branchs = []
        if self.pull_requests:
            for pr_id, pull_request in self.pull_requests.iteritems():
                if not pull_request['base_branch'] in self.branchs:
                    self.branchs.append(pull_request['base_branch'])

        self.branchs.sort(reverse=True)

        return self.branchs

    def _parse_initial_fields(self, pull_request):
        pr_dict = {}
        for field in self.fields:
            if field in pull_request:
                pr_dict[field] = pull_request[field]
            else:
                pr_dict[field] = "None"

        return pr_dict

    def _merge_branch(self, pull_request):
        if ('base' in pull_request) and ('ref' in pull_request['base']):
            return pull_request['base']['ref']
        else:
            return "None"

    def _statuses(self, status):
        statuses = []
        counter = 0
        active = False
        for api_status in status:
            if not self._interesting_status(api_status['description']):
                continue
            elif counter == 0 and api_status['state'] == "pending":
                active = True

            if 'target_url' in api_status:
                status = {}
                status['url'] = api_status['target_url'] if 'target_url' in api_status else ""
                status['description'] = self._parse_description(api_status['description'])
                status['state'] = api_status['state'] if 'state' in api_status else ""
                status['date'] = api_status['created_at'] if 'created_at' in api_status else ""
                status['date'] = status['date'].replace('T', ' ');
                status['date'] = status['date'][:-4]
                status['context'] = api_status['context']

                statuses.append(status)

            counter += 1

        return (statuses, active)

    def _parse_user_info(self, pull_request):
        if 'user' in pull_request:
            if 'login' in pull_request['user']:
                return pull_request['user']['login']

        return 'None'

    def _parse_branch_name(self, pull_request):
        if 'head' in pull_request:
            if 'ref' in pull_request['head']:
                return pull_request['head']['ref']

        return 'None'

    def _build_state(self, pull_request):
        result = 'build-success' if len(pull_request['statuses']) else 'build-none'
        result += ' build-active ' if pull_request['active'] else ''

        result_by_context = {}
        for status in pull_request['statuses']:
          if status['context'] not in result_by_context.keys():
              result_by_context[status['context']] = status['state']

        for status_result in result_by_context.values():
            if status_result == 'failure':
                result = result.replace('success', 'failure')

        return result

    def _parse_description(self, description):
        if 'Merged' in description:
            return "Merging"

        return "Building"

    def _interesting_status (self, status_description):
        return status_description == "Build finished." or status_description == "Merged build finished."

class GitHubConnector:

    def __init__(self, client_id, client_secret, oauth_token, retest_message):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_sufix = '?client_id=' + client_id + '&client_secret=' + client_secret

        self.oauth_token = oauth_token
        self.retest_message = retest_message
        self.headers = {'Authorization': 'token %s' % self.oauth_token}

    def get_pull_requests(self, organization, repository):
        pull_requests_data = []
        api_url = 'https://api.github.com/repos/' + organization + '/' + repository + '/pulls'
        response = requests.get(api_url, headers=self.headers).json()
        for pull_request in response:
            status = self._get_statuses(pull_request)
            pull_requests_data.append((status, pull_request))

        return pull_requests_data

    def retest_pull_request(self, organization, repository, pull_number):
        data = {'body': '%s' % self.retest_message}
        url = 'https://api.github.com/repos/' + organization + '/' + repository
        url += '/issues/' + pull_number + '/comments'

        response = requests.post(url, data=json.dumps(data), headers=self.headers)

        return response.status_code == 201

    def _get_statuses(self, pull_request):
        api_status = []
        if 'statuses_url' in pull_request:
            status_url = pull_request['statuses_url']
            api_status = requests.get(status_url, headers=self.headers).json()
        return api_status

