from typing import Union

from pyrogram import Client
from pyrogram.errors import UserNotParticipant


async def check_participant_channel(tg_client: Client, chat_id: Union[int, str]) -> bool:
    try:
        await tg_client.get_chat_member(chat_id=chat_id, user_id="me")

        return True
    except UserNotParticipant:
        ...
    except Exception:
        ...

    return False
