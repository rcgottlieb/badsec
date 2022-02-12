import json
import sys
import urllib.request
import urllib.response
from hashlib import sha256
from urllib.error import HTTPError
from urllib.parse import urljoin

connection_attempts = 0
base_url = 'http://0.0.0.0:8888'


def connect_and_print_user_ids():
    auth_token = get_auth_token()
    user_ids = get_userids(auth_token)
    print(user_ids)


def get_userids(auth_token) -> str:
    """
    This function return's a json representation of the requested user ids as a json array of strings
    :rtype: object
    :param auth_token: is the authorization token retrieved from the server to use in the request for the users
    """
    user_ids = ""
    user_headers = dict()
    user_headers['X-Request-Checksum'] = auth_token
    users_url = urljoin(base_url, "/users")
    users_request = urllib.request.Request(users_url, headers=user_headers, method='GET')

    if users_request and auth_token:
        users_response = connect_with_request(users_request)
        # convert the lines to a list of json strings
        lines = users_response.readlines()
        user_ids: str = json.dumps(list(line.decode('utf-8').strip() for line in lines))
    return user_ids


def get_auth_token():
    global base_url
    auth_url = urljoin(base_url, "/auth")
    auth_request = urllib.request.Request(auth_url, method='HEAD')
    auth_response = connect_with_request(auth_request)
    auth_token_header = auth_response.headers['Badsec-Authentication-Token']

    auth_token_header_str = auth_token_header + "/users"
    auth_token_sha256 = sha256(auth_token_header_str.encode('utf-8'))
    auth_token = auth_token_sha256.digest().hex()
    return auth_token


def connect_with_request(request):
    a_response, succeeded = connect_to_badsec_server_using_request(request)
    global connection_attempts
    while connection_attempts < 3:
        if not succeeded:
            print("failed to connect retrying...")
            a_response, succeeded = connect_to_badsec_server_using_request(request)
        else:
            return a_response
    print("The connection timed out")
    sys.exit(-1)


def connect_to_badsec_server_using_request(a_request):
    succeeded = True
    server_response = None

    if not a_request:
        print("A valid request is needed", file=sys.stderr)
        return None, False

    try:
        server_response = urllib.request.urlopen(a_request)
    except urllib.error.HTTPError as http_error:
        succeeded = False
        if http_error.code == 401:
            print("Unauthorized access", file=sys.stderr)
        elif http_error.code == 404:
            print("URL not found", file=sys.stderr)
    except urllib.error.URLError as error_response:
        succeeded = False
        global connection_attempts
        connection_attempts += 1
        print("URL Error: ", error_response.reason, file=sys.stderr)

    return server_response, succeeded


if __name__ == "__main__":
    # Call the function that starts it all
    connect_and_print_user_ids()
