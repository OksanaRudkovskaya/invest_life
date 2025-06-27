from settings.load_config import load_config

config = load_config('settings/config.yml')

TELEGRAM_BOT_TOKEN = config.get('telegram', {}).get('bot_token')
TELEGRAM_CHAT_IDS = config.get('telegram', {}).get('chat_ids')

FASTAPI_VERIFY_TOKEN_MIDDLEWARE = config.get('fastapi', {}).get('VERIFY_TOKEN_MIDDLEWARE')
FASTAPI_TOKEN_HEADER = config.get('fastapi', {}).get('TOKEN_HEADER')

