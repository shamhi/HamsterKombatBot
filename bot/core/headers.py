import random
from typing import Dict

from fake_useragent import UserAgent


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


def get_headers() -> Dict[str, str]:
    """
    Generate headers for HTTP requests.

    :return: dictionary containing headers
    """
    android_version = random.randint(24, 33)
    webview_version = random.randint(70, 125)

    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'ru-RU,ru;q=0.9',
        'Content-Type': 'application/json',
        'Connection': 'keep-alive',
        'Origin': 'https://hamsterkombat.io',
        'Referer': 'https://hamsterkombat.io/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Ch-Ua': f'"Android WebView";v="{webview_version}", "Chromium";v="{webview_version}", "Not?A_Brand";v="{android_version}"',
        'Sec-Ch-Ua-mobile': '?1',
        'Sec-Ch-Ua-platform': '"Android"',
        'User-Agent': get_mobile_user_agent(),
    }
    return headers
