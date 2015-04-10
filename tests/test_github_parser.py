import unittest
import test_data

from github_helper import GitHubParser

class TestGithubParser(unittest.TestCase):

    def setUp(self):
        self.github_parser = GitHubParser()
        self.github_parser.add_pull_requests(test_data.fake_pull_requests_data,"Zentyal","Openchange")

    def test_add_pull_requests_len_1(self):
        self.assertEqual(1, len(self.github_parser.get_pull_requests()))

    def test_active_status(self):
        pull = self.github_parser.get_pull_requests().values()[0]
        self.assertEqual(False, pull['active'])

    def test_number_of_statuses(self):
        pull = self.github_parser.get_pull_requests().values()[0]
        self.assertEqual(1, len(pull['statuses']))

    def test_build_state(self):
        pull = self.github_parser.get_pull_requests().values()[0]
        self.assertEqual('build-success', pull['build_state'])

    def test_statuses_active(self):
        statuses, active = self.github_parser._statuses(test_data.fake_good_status_data)
        self.assertEqual(False, active)

    def test_statuses_num_status(self):
        statuses, active = self.github_parser._statuses(test_data.fake_failed_status_data)
        self.assertEqual(4,len(statuses))

    def test_statuses_num_status_true(self):
        statuses, active = self.github_parser._statuses(test_data.fake_good_status_data)
        self.assertEqual(7,len(statuses))

    def test_build_state_should_fail_but_last_one_is_good(self):
        statuses, active = self.github_parser._statuses(test_data.fake_tricky_status_data)
        pull_request_dict = {}
        pull_request_dict['statuses'] = statuses
        pull_request_dict['active'] = active
        self.assertEqual('build-failure',self.github_parser._build_state(pull_request_dict))

    def test_build_state_should_pass(self):
        statuses, active = self.github_parser._statuses(test_data.fake_good_status_data)
        pull_request_dict = {}
        pull_request_dict['statuses'] = statuses
        pull_request_dict['active'] = active
        self.assertEqual('build-success',self.github_parser._build_state(pull_request_dict))

    def test_build_state_should_fail(self):
        statuses, active = self.github_parser._statuses(test_data.fake_failed_status_data)
        pull_request_dict = {}
        pull_request_dict['statuses'] = statuses
        pull_request_dict['active'] = active
        self.assertEqual('build-failure',self.github_parser._build_state(pull_request_dict))

    def test_build_state_should_work_if_no_status(self):
        statuses, active = self.github_parser._statuses(test_data.fake_failed_status_data)
        pull_request_dict = {}
        pull_request_dict['statuses'] = []
        pull_request_dict['active'] = active
        self.assertEqual('build-none',self.github_parser._build_state(pull_request_dict))
