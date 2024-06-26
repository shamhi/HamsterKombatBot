from discord_webhook import DiscordWebhook
from bot.config import settings
from bot.utils.logger import logger

# avatar = "https://static9.tgcnt.ru/posts/_0/8b/8b90de800cdeb8557c9fa7a6c04ad8cf.jpg"

def discord_msg(session_name:str,msg:str):
    try:
        
        webhook = DiscordWebhook(
        url=settings.DISCORD_WEEBHOOK_URL,
        content=msg,
        username=session_name,
        # avatar_url=avatar
        )
        response = webhook.execute()
        if response.status_code != 200:
            logger.error(f"{session_name} | Failed to send to Discord: {response.status_code}")
            
    except Exception as e:
       logger.error(f"{session_name} | Failed to send to Discord: {e}")
