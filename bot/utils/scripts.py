import json
import hashlib
import random
import string


def generate_random_visitor_id():
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    visitor_id = hashlib.md5(random_string.encode()).hexdigest()

    return visitor_id


def escape_html(text: str) -> str:
    return text.replace('<', '\\<').replace('>', '\\>')


def get_auth_key(session_name: str) -> str | None:
    try:
        with open('auth_keys.json', 'r', encoding="utf-8") as file:
            auth_keys = json.load(file)

        auth_key = auth_keys.get(session_name)
        return auth_key
    except FileNotFoundError:
        return None


def save_auth_key(session_name: str, auth_key: str) -> None:
    try:
        with open('auth_keys.json', 'r', encoding="utf-8") as file:
            auth_keys = json.load(file)
    except FileNotFoundError:
        auth_keys = {}

    auth_keys[session_name] = auth_key
    with open('auth_keys.json', 'w', encoding="utf-8") as file:
        json.dump(auth_keys, file, indent=4, ensure_ascii=False)
