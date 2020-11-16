from lib.config import config
from lib.bot import bot

VERSION = config.get_value('version')

bot.run(VERSION)