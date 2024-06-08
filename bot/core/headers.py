import random

from fake_useragent import UserAgent


def get_mobile_user_agent():
    ua = UserAgent(platforms=['mobile'])
    return ua.random


def get_headers():
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
        'Sec-Ch-Ua': f'"Google Chrome";v="{random.randint(70, 125)}", "Chromium";v="{random.randint(70, 125)}", "Not.A/Brand";v="{random.randint(10, 30)}"',
        'Sec-Ch-Ua-mobile': '?1',
        'Sec-Ch-Ua-platform': '"Android"',
        'User-Agent': get_mobile_user_agent()
    }
    return headers
