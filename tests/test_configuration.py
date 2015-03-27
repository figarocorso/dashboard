import unittest

from configuration import ConfigurationParser

class TestConfiguration(unittest.TestCase):

    def setUp(self):
        self.configuration = ConfigurationParser('dashboard.conf')
        pass

    def test_refresh_rate(self):
        self.assertEqual(600, self.configuration.refresh_rate())

    def test_github_repositories(self):
        repositories = self.configuration.github_repositories()
        self.assertEqual(5, len(repositories))

        self.assertEqual('Zentyal', repositories[0]['organization'])
        self.assertEqual('sogo', repositories[1]['repository'])

    def test_blacklist(self):
        blacklist = self.configuration.jenkins_blacklist()
        self.assertEqual(4, len(blacklist))

        self.assertEqual('_qa', blacklist[2])
