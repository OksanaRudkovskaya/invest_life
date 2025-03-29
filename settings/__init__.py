from pathlib import Path
from environs import Env

ROOT_PATH = Path(__file__).parent.parent.resolve()
ENV_PATH = str(ROOT_PATH / 'settings' / '.env')

env = Env()
env.read_env(ENV_PATH)
PG_HOST = env.str('PG_HOST')
PG_PORT = env.str('PG_PORT')
PG_USER = env.str('PG_USER')
PG_PASSWORD = env.str('PG_PASSWORD')
PG_DATABASE = env.str('PG_DATABASE')

TINKOFF_TOKEN = env.str('TINKOFF_TOKEN')
