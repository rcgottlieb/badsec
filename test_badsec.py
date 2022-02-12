import unittest
import urllib
import urllib.request
import badsec


class MyTestCase(unittest.TestCase):

    def test_connect_to_covid_server_using_request(self):
        headers = dict()
        headers['accept'] = 'application/json'
        headers['User-Agent'] = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:48.0) Gecko/20100101 Firefox/48.0"
        states_url = 'https://disease.sh/v3/covid-19/states'

        auth_request = urllib.request.Request(states_url, headers=headers, method='GET')
        auth_response, succeeded = badsec.connect_to_badsec_server_using_request(auth_request)
        self.assertTrue(auth_response.code, 200)
        self.assertTrue(True, succeeded)

    def test_connect_to_badsec_server_using_request(self):
        auth_token = badsec.get_auth_token()
        user_ids = badsec.get_userids(auth_token)
        self.assertTrue(len(user_ids) > 0)

    def test_connect_to_covid_server_using_bad_request(self):
        headers = dict()
        headers['accept'] = 'application/json'
        headers['User-Agent'] = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:48.0) Gecko/20100101 Firefox/48.0"
        bad_url = 'https://disease.sh/v3/covid-19/state'

        auth_request = urllib.request.Request(bad_url, headers=headers, method='GET')
        auth_response, succeeded = badsec.connect_to_badsec_server_using_request(auth_request)
        self.assertIsNone(auth_response)
        self.assertFalse(succeeded)

    def test_connect_with_bad_request(self):
        server_response, succeeded = badsec.connect_to_badsec_server_using_request(None)
        self.assertIsNone(server_response)

    def test_get_users_response_no_token(self):
        auth_token = None
        json_string = badsec.get_userids(auth_token)
        self.assertTrue(len(json_string) <= 0, "json_string is missing or malformed")


if __name__ == '__main__':
    unittest.main()
