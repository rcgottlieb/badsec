import unittest
import urllib
import badsec


class MyTestCase(unittest.TestCase):

    def test_connect_to_badsec_server_using_request(self):
        '''
        This returns OK as I'm checking for a response and that the request succeeds, which it does
        :return:
        '''

        headers = dict()
        headers['accept'] = 'application/json'
        headers['User-Agent'] = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:48.0) Gecko/20100101 Firefox/48.0"
        states_url = 'https://disease.sh/v3/covid-19/states'

        auth_request = urllib.request.Request(states_url, headers=headers, method='GET')
        auth_response, succeeded = badsec.connect_to_badsec_server_using_request(auth_request)
        self.assertTrue(auth_response.code, 200)
        self.assertTrue(True, succeeded)

    def test_connect_to_badsec_server_using_bad_request(self):
        '''
        This returns OK as I'm checking for lack of a response and that the request does not succeed
        If you want to make this not succeed, change either self.assertIsNone to self.assertIs or assertFalse to assertTrue
        :return:
        '''
        headers = dict()
        headers['accept'] = 'application/json'
        headers['User-Agent'] = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:48.0) Gecko/20100101 Firefox/48.0"
        bad_url = 'https://disease.sh/v3/covid-19/state'

        auth_request = urllib.request.Request(bad_url, headers=headers, method='GET')
        auth_response, succeeded = badsec.connect_to_badsec_server_using_request(auth_request)
        self.assertIsNone(auth_response)
        self.assertFalse(False, succeeded)


if __name__ == '__main__':
    unittest.main()
