from asyncio.tasks import sleep
from datetime import datetime
from unicodedata import *
from glob import glob

from discord.ext.commands.errors import BadArgument, CommandNotFound, MissingRequiredArgument
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import Context
from discord.errors import Forbidden
from discord import Intents, Embed

from lib.config import config
from lib.db import db

COGS = [path.split('\\')[-1][:-3] for path in glob('./lib/cogs/*.py')]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)
OWNER_IDS = config.get_value('ownerids')
PREFIX = config.get_value('prefix')

class Ready(object):
    def __init__(self) -> None:
        for cog in COGS:
            setattr(self, cog, False)
    
    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f'{cog.capitalize()} cog ready')
    
    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
    def __init__(self) -> None:
        self.PREFIX = PREFIX
        
        self.guild = None
        self.ready = False
        self.cogs_ready = Ready()
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)

        super().__init__(
            command_prefix=PREFIX, 
            owner_ids=OWNER_IDS,
            intents=Intents.all()
        )
    
    def setup(self):
        print('Loading cogs...')

        for cog in COGS:
            self.load_extension(f'lib.cogs.{cog}')
            print(f'{cog.capitalize()} cog loaded')
        
        print('Setup complete')
    
    def run(self, version):
        self.VERSION = version

        print('Running setup...')
        self.setup()

        with open('./lib/bot/token.0', 'r', encoding='utf-8') as tf:
            self.TOKEN = tf.read()

        print('Starting...')

        super().run(self.TOKEN, reconnect=True)

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)

        if ctx.command is not None and ctx.guild is not None:
            if not self.ready:
                await ctx.send('Not ready yet, please wait...')
            else:
                await ctx.message.delete()
                await self.invoke(ctx)
    
    async def on_connect(self):
        print('Connected')

    async def on_disconnect(self):
        print('Disconnected')
    
    async def on_error(self, err, *args, **kwargs):
        if err == 'on_command_error':
            await args[0].send('Something went wrong')

        raise Exception('An error occured')

    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
            pass
        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send('One or more required arguments missing')
        elif hasattr(exc, 'original'):
            if isinstance(exc.original, Forbidden):
                await ctx.send('I don\'t have the permission to do that')
            else:
                raise exc.original
        else:
            raise exc
    
    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(581609258525655041)
            self.channel = self.get_channel(581609258525655043)

            self.scheduler.start()

            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            self.ready = True

            print('Bot ready')

            embed = Embed(title='Status: Online', description='Xenon is now online', colour=0x20A050, timestamp=datetime.utcnow())

            embed.add_field(name='Command Prefix', value=f'{name(PREFIX).lower().capitalize()} : {PREFIX}', inline=False)

            await self.channel.send(embed=embed)
        else:
            print('Reconnected')

    async def on_message(self, msg):
        if not msg.author.bot:
            await self.process_commands(msg)

bot = Bot()