import os
import glob
import random
import string
import base64
import asyncio
import hashlib

import aiohttp
from fake_useragent import UserAgent
from playwright.async_api import async_playwright

from bot.config import settings
from bot.utils.logger import logger
from bot.utils.json_db import JsonDB
from bot.utils.default import DEFAULT_HEADERS, DEFAULT_FINGERPRINT


def get_session_names():
    names = [os.path.splitext(os.path.basename(file))[0] for file in glob.glob('sessions/*.session')]

    return names


def generate_random_visitor_id():
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=32))

    visitor_id = hashlib.md5(random_string.encode()).hexdigest()

    return visitor_id


def escape_html(text: str):
    return text.replace('<', '\\<').replace('>', '\\>')


def decode_cipher(cipher: str):
    encoded = cipher[:3] + cipher[4:]
    return base64.b64decode(encoded).decode('utf-8')


def get_headers(name: str):
    db = JsonDB("profiles")

    profiles = db.get_data()

    headers = profiles.get(name, {}).get('headers', DEFAULT_HEADERS)

    if settings.USE_RANDOM_USERAGENT:
        android_version = random.randint(24, 33)
        webview_version = random.randint(70, 125)

        headers['Sec-Ch-Ua'] = (
            f'"Android WebView";v="{webview_version}", '
            f'"Chromium";v="{webview_version}", '
            f'"Not?A_Brand";v="{android_version}"'
        )
        headers['User-Agent'] = get_mobile_user_agent()

    return headers


def get_fingerprint(name: str):
    db = JsonDB("profiles")

    profiles = db.get_data()

    fingerprint = profiles.get(name, {}).get('fingerprint', DEFAULT_FINGERPRINT)

    fingerprint['visitorId'] = generate_random_visitor_id()

    return fingerprint


def get_mobile_user_agent():
    ua = UserAgent(platforms=['mobile'], os=['android'])
    user_agent = ua.random
    if 'wv' not in user_agent:
        parts = user_agent.split(')')
        parts[0] += '; wv'
        user_agent = ')'.join(parts)
    return user_agent


async def get_mini_game_cipher(http_client: aiohttp.ClientSession, user_id: int, session_name: str, start_date: str):
    response = await http_client.get(url="https://hamsterkombatgame.io/games/UnblockPuzzle/?v")
    original_html = await response.text()

    search_script = '''<script id="engine-start" type="text/javascript" merge="keep">Module.persistentStorage=!1;EngineLoader.load("canvas","DefoldGames");function onSandboxMessage(e){let a="string"==typeof e.data?JSON.parse(e.data):e.data;a&&"StartGame"===a.method&&JsToDef.send("__StartGame",a)}function OnGameFinished(e){parent.postMessage(JSON.stringify({method:"OnGameFinished",cipher:e}))}function OnSceneLoaded(){parent.postMessage(JSON.stringify({method:"OnSceneLoaded"}))}window.addEventListener("message",onSandboxMessage,!1)</script>'''
    replace_script = f'''<script id="engine-start" type="text/javascript" merge="keep">Module.persistentStorage=!1;EngineLoader.load("canvas","DefoldGames");function onSandboxMessage(e){{let a={{method: "StartGame",level: "- - - - - -.- - - - - -.0 0 - - - -.- - - - - -.- - - - - -.- - - - - -",number: new Date("{start_date}").getTime() / 1e3}};a && "StartGame" === a.method && JsToDef.send("__StartGame",a);}}function OnGameFinished(e) {{let hiddenElement = document.createElement('div');hiddenElement.id = 'gameKeyElement';hiddenElement.style.display = 'none';hiddenElement.setAttribute('data-game-key', e);document.body.appendChild(hiddenElement);}}function OnSceneLoaded() {{parent.postMessage(JSON.stringify({{method:"OnSceneLoaded"}}))}}window.addEventListener("message",onSandboxMessage,!1)</script>'''
    modified_html = original_html.replace(search_script, replace_script)

    async with async_playwright() as driver:
        browser = await driver.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 500, 'height': 500})

        page = await context.new_page()
        await page.set_content(modified_html)

        actions = [
            {'type': 'mousemove', 'x': 100, 'y': 228, 'timestamp': 1721665313608},
            {'type': 'mousemove', 'x': 100, 'y': 229, 'timestamp': 1721665313614},
            {'type': 'mousemove', 'x': 99, 'y': 230, 'timestamp': 1721665313620},
            {'type': 'mousemove', 'x': 99, 'y': 231, 'timestamp': 1721665313626},
            {'type': 'mousemove', 'x': 98, 'y': 232, 'timestamp': 1721665313632},
            {'type': 'mousemove', 'x': 98, 'y': 233, 'timestamp': 1721665313638},
            {'type': 'mousemove', 'x': 98, 'y': 234, 'timestamp': 1721665313644},
            {'type': 'mousemove', 'x': 97, 'y': 234, 'timestamp': 1721665313650},
            {'type': 'mousemove', 'x': 96, 'y': 235, 'timestamp': 1721665313656},
            {'type': 'mousemove', 'x': 96, 'y': 236, 'timestamp': 1721665313663},
            {'type': 'mousemove', 'x': 95, 'y': 237, 'timestamp': 1721665313675},
            {'type': 'mousemove', 'x': 94, 'y': 238, 'timestamp': 1721665313687},
            {'type': 'mousemove', 'x': 93, 'y': 239, 'timestamp': 1721665313706},
            {'type': 'mousemove', 'x': 93, 'y': 240, 'timestamp': 1721665313711},
            {'type': 'mousemove', 'x': 92, 'y': 241, 'timestamp': 1721665313723},
            {'type': 'mousemove', 'x': 92, 'y': 242, 'timestamp': 1721665313735},
            {'type': 'mousedown', 'x': 92, 'y': 242, 'timestamp': 1721665313802},
            {'type': 'mouseup', 'x': 92, 'y': 242, 'timestamp': 1721665313878}
        ]

        start_time = actions[0]['timestamp']
        await page.mouse.move(0, 0)

        for action in actions:
            delay = (action['timestamp'] - start_time) / 1000.0
            await asyncio.sleep(delay=delay)

            start_time = action['timestamp']
            if action['type'] == 'mousedown':
                await page.mouse.move(action['x'], action['y'])
                await page.mouse.down()
            elif action['type'] == 'mousemove':
                await page.mouse.move(action['x'], action['y'])
            elif action['type'] == 'mouseup':
                await page.mouse.move(action['x'], action['y'])
                await page.mouse.up()

        await asyncio.sleep(delay=2)

        try:
            game_key = await page.evaluate('document.querySelector("#gameKeyElement")?.getAttribute("data-game-key")')

            if game_key:
                logger.info(f"{session_name} | Key for Mini Game: <lc>{game_key}</lc>")

                cipher = game_key.strip()
                body = f"{cipher}|{user_id}"
                encoded_body = base64.b64encode(body.encode()).decode()

                return encoded_body
            else:
                logger.error(f"Key for Mini Game is not found: <lr>{game_key}</lr>")
        except Exception as error:
            logger.error(f"Error while getting key for Mini Game: {error}")

        await browser.close()

        return ''
