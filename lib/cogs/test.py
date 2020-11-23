from discord.ext.commands import command
from discord.ext.commands import Cog

class Test(Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @command(name='test', aliases=['t'])
    async def test_command(self, ctx):
        await ctx.send(f'This test command was run by {ctx.author.mention}')

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('test')

def setup(bot):
    bot.add_cog(Test(bot))