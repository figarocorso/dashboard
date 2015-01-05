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
