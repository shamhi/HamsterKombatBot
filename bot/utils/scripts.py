import json


def get_auth_key(session_name: str) -> str | None:
    try:
        with open('auth_keys.json', 'r') as file:
            auth_keys = json.load(file)

        auth_key = auth_keys.get(session_name)
        return auth_key
    except FileNotFoundError:
        return None


def save_auth_key(session_name: str, auth_key: str) -> None:
    try:
        with open('auth_keys.json', 'r') as file:
            auth_keys = json.load(file)
    except FileNotFoundError:
        auth_keys = {}

    auth_keys[session_name] = auth_key
    with open('auth_keys.json', 'w', encoding="utf-8") as file:
        json.dump(auth_keys, file, indent=4, ensure_ascii=False)
