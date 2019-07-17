import json
import unittest
from app.routes import app


class ApiTestCases(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.attrs_list = ['public_repos_count', 'forked_repos_count', 'followers_count', 'original_repos_count',
                           'list_languages', 'repos']

    def test_team_request_response_ok(self):
        response = self.app.get('/api/v1/teams/pygame')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        for attr in self.attrs_list:
            self.assertTrue(attr in data.keys())

    def test_team_request_response_error(self):
        response = self.app.get('/api/v1/teams/pygameeeeeeee')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertTrue('error' in data.keys())

    def test_merged_orgs_team_request_ok(self):
        response = self.app.get('/api/v1/orgs/mailchimp/teams/pygame')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        for attr in self.attrs_list:
            self.assertTrue(attr in data.keys())

    def test_merged_orgs_team_request_error(self):
        response = self.app.get('/api/v1/orgs/samesame/teams/same')

        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertTrue('error' in data.keys())
