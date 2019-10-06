"""spotify_token

Retrieves a web player access_token from Spotify

Written by Alex Ladd http://github.com/AlexLadd

Original Code from spotify_token: https://github.com/enriquegh/spotify-webplayer-token
License: MIT https://github.com/enriquegh/spotify-webplayer-token/blob/master/LICENSE

Contributors:
Daniel Lashua http://github.com/dlashua

Updated: 2019-10-04
"""

import os
import requests
from bs4 import BeautifulSoup
import json

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"


def _get_csrf(session, cookies):
    """ Get CSRF token for Spotify login. """
    headers = {'user-agent': USER_AGENT}
    response = session.get("https://accounts.spotify.com/login",
                           headers=headers, cookies=cookies)
    response.raise_for_status()
    return response.cookies['csrf_token']


def _login(session, cookies, username, password, csrf_token):
    """ Logs in with CSRF token and cookie within session. """
    headers = {'user-agent': USER_AGENT}

    data = {"remember": False, "username": username, "password": password,
            "csrf_token": csrf_token}

    response = session.post("https://accounts.spotify.com/api/login",
                            data=data, cookies=cookies, headers=headers)

    response.raise_for_status()


def _get_access_token(session, cookies):
    """ Gets access token after login has been successful. """
    headers = {'user-agent': USER_AGENT}

    response = session.get("https://open.spotify.com/browse",
                           headers=headers, cookies=cookies)
    response.raise_for_status()

    data = response.content.decode("utf-8")

    xml_tree = BeautifulSoup(data, 'lxml')
    script_node = xml_tree.find("script", id="config")
    config = json.loads(script_node.string)

    access_token = config['accessToken']
    expiration = config['accessTokenExpirationTimestampMs']
    expiration_date = int(expiration) // 1000

    return access_token, expiration_date


def start_session(username=None, password=None):
    """ Starts session to get access token. """

    # arbitrary value and can be static
    cookies = {"__bon": "MHwwfC01ODc4MjExMzJ8LTI0Njg4NDg3NTQ0fDF8MXwxfDE="}

    if username is None:
        username = os.getenv("SPOTIFY_USERNAME")

    if password is None:
        password = os.getenv("SPOTIFY_PASS")

    if username is None or password is None:
        raise Exception("No username or password")

    session = requests.Session()
    token = _get_csrf(session, cookies)

    _login(session, cookies, username, password, token)
    access_token, expiration_date = _get_access_token(session, cookies)

    data = [access_token, expiration_date]
    return data