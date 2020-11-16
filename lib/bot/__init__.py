from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase

PREFIX = '~'
OWNER_IDS = [108298219003346944]

class Bot(BotBase):
    def __init__(self) -> None:
        self.PREFIX = PREFIX
        
        self.guild = None
        self.ready = False
        self.scheduler = AsyncIOScheduler()

        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS)
    
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
    
    async def on_ready(self):
        if not self.ready:
            self.ready = True
            # self.guild = self.get_guild(581609258525655041)

            print('Ready')
        else:
            print('Reconnected')

    async def on_message(self, msg):
        pass

bot = Bot()