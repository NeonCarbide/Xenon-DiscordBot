from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands.errors import CommandNotFound
from discord.ext.commands import Bot as BotBase
from discord import Intents, Embed

from lib.config import config

PREFIX = config.get_value('prefix')
OWNER_IDS = config.get_value('ownerids')

class Bot(BotBase):
    def __init__(self) -> None:
        self.PREFIX = PREFIX
        
        self.guild = None
        self.ready = False
        self.scheduler = AsyncIOScheduler()

        super().__init__(
            command_prefix=PREFIX, 
            owner_ids=OWNER_IDS,
            intents=Intents.all()
        )
    
    def run(self, version):
        self.VERSION = version

        with open('./lib/bot/token.0', 'r', encoding='utf-8') as tf:
            self.TOKEN = tf.read()

        print('Running...')

        super().run(self.TOKEN, reconnect=True)
    
    async def on_connect(self):
        print('Connected')

    async def on_disconnect(self):
        print('Disconnected')
    
    async def on_error(self, err, *args, **kwargs):
        if err == 'on_command_error':
            await args[0].send('Something went wrong')

        raise err

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            pass
        elif hasattr(exc, 'original'):
            raise exc.original
        else:
            raise exc
    
    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(581609258525655041)

            print('Ready')

            channel = self.get_channel(581609258525655043)
            embed = Embed(title='Status: Online', description='Xenon is now online', colour=0x20A050, timestamp=datetime.utcnow())

            await channel.send(embed=embed)
        else:
            print('Reconnected')

    async def on_message(self, msg):
        pass

bot = Bot()