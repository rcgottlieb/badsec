import json
import sys
import urllib.request
import urllib.response
from hashlib import sha256
from urllib.error import HTTPError

connection_attempts = 0
base_url = 'http://0.0.0.0:8888'


def connect_and_print_user_ids():
    auth_token = get_auth_token()
    user_ids = get_users_response(auth_token)
    print_users_json(user_ids)


def get_users_response(auth_token) -> str:
    """
    This function return's a json representation of the requested user ids as a python list of strings
    :param auth_token: is the token retrieved from the server using get_auth_token().
    """
    json_lines = []
    user_headers = dict()
    user_headers['X-Request-Checksum'] = auth_token
    users_url = base_url + '/users'
    users_request = urllib.request.Request(users_url, headers=user_headers, method='GET')
    users_response = connect_with_request(users_request)

    # convert the lines to a list of python strings
    lines = users_response.readlines()
    for line in lines:
        json_line = line.decode('utf-8').strip()
        json_lines.append(json_line)
    user_ids: str = json.dumps(json_lines)
    return user_ids


def get_auth_token():
    global base_url
    auth_url = base_url + "/auth"
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
    try:
        server_response = urllib.request.urlopen(a_request)
    except urllib.error.HTTPError as http_error:
        succeeded = False
        if http_error.code == 401:
            print("Unauthorized access", file=sys.stderr)
        elif http_error.code == 404:
            print("URL not found", file=sys.stderr)
        print("error_response reason: ", http_error.reason, file=sys.stderr)
    except urllib.error.URLError as error_response:
        succeeded = False
        global connection_attempts
        connection_attempts += 1
        print("URL Error: ", error_response.reason, file=sys.stderr)

    return server_response, succeeded


def print_users_json(user_ids):
    print(user_ids)


if __name__ == "__main__":
    # Call the function that starts it all
    connect_and_print_user_ids()
