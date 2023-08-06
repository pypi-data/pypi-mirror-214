import logging

from aiohttp.web import Application

from .bot import Bot
from .config import BOT_TOKEN, MONGO, APP_URL
from .deps import MongoStorage
from .dispatcher import Dispatcher

storage = MongoStorage(
    db_name=MONGO.DB,
    host=MONGO.HOST,
    username=MONGO.USER,
    password=MONGO.PASSWORD,
)

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot, storage)
logger = logging.getLogger()
app = Application()

Dispatcher.set_current(dp)


def run():
    dp.run_server(APP_URL, app)
