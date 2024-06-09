import json
import random
import string
import base64
import hashlib
import time


def generate_random_visitor_id():
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    visitor_id = hashlib.md5(random_string.encode()).hexdigest()

    return visitor_id


def escape_html(text: str) -> str:
    return text.replace('<', '\\<').replace('>', '\\>')


def decode_cipher(cipher: str) -> str:
    encoded = cipher[:3] + cipher[4:]
    return base64.b64decode(encoded).decode('utf-8')


def get_headers(name: str):
    try:
        with open('profile.json', 'r') as file:
            profile = json.load(file)
    except:
        profile = {}

    headers = profile.get(name, {}).get('headers', {})

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


def convert_seconds_to_formatted_time(Number: int) -> str:
    """converts a number of seconds to a formatted string with this format:
    H Hours & M Minutes & S Seconds
    """
    Hours = Number // 3600
    Minutes = (Number % 3600) // 60
    Seconds = (Number % 3600) % 60
    
    if Hours == 0:
        if Minutes == 0:
            result = f"{Seconds} Seconds"
        else:
            result = f"{Minutes} Minutes & {Seconds} Seconds"
    else:
        result = f"{Hours} Hours & {Minutes} Minutes & {Seconds} Seconds"

    return result


def calculate_start_time(delay_seconds: int) -> str:
    """calculates when the bot will start clicking again after a delay (in seconds).
    """
    current_time = time.time()
    start_time = current_time + delay_seconds
    start_time_formatted = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
    return start_time_formatted

