import hashlib
import json
import random
import string
import base64
from fake_useragent import UserAgent


def generate_random_visitor_id():
    random_string = ''.join(
        random.choices(string.ascii_letters + string.digits, k=32)
    )
    visitor_id = hashlib.md5(random_string.encode()).hexdigest()

    return visitor_id


def escape_html(text: str) -> str:
    return text.replace('<', '\\<').replace('>', '\\>')


def decode_cipher(cipher: str) -> str:
    encoded = cipher[:3] + cipher[4:]
    return base64.b64decode(encoded).decode('utf-8')


def get_mobile_user_agent() -> str:
    """
    Function: get_mobile_user_agent

    This method generates a random mobile user agent for an Android platform.
    If the generated user agent does not contain the "wv" string,
    it adds it to the browser version component.

    :return: A random mobile user agent for Android platform.
    """
    ua = UserAgent(platforms=['mobile'], os=['android'])
    user_agent = ua.random
    if 'wv' not in user_agent:
        parts = user_agent.split(')')
        parts[0] += '; wv'
        user_agent = ')'.join(parts)
    return user_agent


def get_headers(name: str):
    try:
        with open('profile.json', 'r') as file:
            profile = json.load(file)
    except:
        profile = {}
    android_version = random.randint(24, 33)
    webview_version = random.randint(70, 125)
    headers = profile.get(name, {}).get('headers', {})
    headers['Sec-Ch-Ua'] = (
        f'"Android WebView";v="{webview_version}", '
        f'"Chromium";v="{webview_version}", '
        f'"Not?A_Brand";v="{android_version}"'
    )
    headers['User-Agent'] = get_mobile_user_agent()
    return headers


def get_fingerprint(name: str):
    try:
        with open('profile.json', 'r') as file:
            profile = json.load(file)
    except:
        profile = {}

    fingerprint = profile.get(name, {}).get('fingerprint', {})

    fingerprint['visitorId'] = generate_random_visitor_id()

    return fingerprint
