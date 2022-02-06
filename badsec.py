from hashlib import sha256
import json
import sys
import urllib.request
import urllib.response
from urllib.error import HTTPError

connection_attempts = 0
base_url = 'http://0.0.0.0:8888'


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


def connect_and_print_user_ids():
    # first get the authorization token
    global base_url
    auth_url = base_url + "/auth"
    auth_request = urllib.request.Request(auth_url, method='HEAD')
    auth_response = connect_with_request(auth_request)
    auth_token_header = auth_response.headers['Badsec-Authentication-Token']

    # Set up headers for users request
    auth_token_header_str = auth_token_header + "/users"
    auth_token_sha256 = sha256(auth_token_header_str.encode('utf-8'))
    auth_token = auth_token_sha256.digest().hex()

    user_headers = dict()
    user_headers['X-Request-Checksum'] = auth_token
    users_url = base_url + '/users'

    # Request the users
    users_request = urllib.request.Request(users_url, headers=user_headers, method='GET')
    users_response = connect_with_request(users_request)
    print_users_json(users_response)


def print_users_json(response):
    """
    One improvement here is to pretty print the output. I'm following directions,
    and it is just a series of user ids. Normally I would iterate over the lines and print
    them formatted based on the data format

    :param response: is used to bring in the results from the REST request.
    """
    # Need to decode each userid, strip the newline and then add it back to a list before converting to json
    json_lines = []
    lines = response.readlines()
    for line in lines:
        new_line = line.decode('utf-8').strip()
        json_lines.append(new_line)
    print(json.dumps(json_lines))


def connect_to_badsec_server_using_request(a_request):
    succeeded = True
    server_response = None
    try:
        server_response = urllib.request.urlopen(a_request)
    except urllib.error.HTTPError as error_response:
        succeeded = False
        global connection_attempts
        connection_attempts += 1
        print("connection_attempt #", connection_attempts, file=sys.stderr)
        print("error_response code: ", error_response.code, file=sys.stderr)
        print("error_response reason: ", error_response.reason, file=sys.stderr)
    return server_response, succeeded


def connection_succeeded(response):
    succeeded = True
    if type(response) == urllib.error.HTTPError:
        succeeded = False
        global connection_attempts
        connection_attempts += 1
        print(f"connection_attempts is {connection_attempts}")
    return succeeded


if __name__ == "__main__":
    # Call the function that starts it all
    connect_and_print_user_ids()
