import hashlib
import random
import string


def generate_random_visitor_id():
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    visitor_id = hashlib.md5(random_string.encode()).hexdigest()

    return visitor_id


def escape_html(text: str) -> str:
    return text.replace('<', '\\<').replace('>', '\\>')
