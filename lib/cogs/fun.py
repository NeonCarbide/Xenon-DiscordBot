from typing import Optional

from discord.ext.commands.errors import BadArgument
from discord.ext.commands import command
from discord.ext.commands import Cog
from discord import Member

class Fun(Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @command(name='stinkeye', aliases=['stink', 'se'])
    async def give_stinkeye(self, ctx, member: Member, *, reason: Optional[str] = 'for absolutely no reason at all!'):
        await ctx.send(f'{ctx.author.display_name} has given {member.mention} the stink eye {reason}')
    
    @give_stinkeye.error
    async def give_stinkeye_error(self, ctx, exc):
        if isinstance(exc, BadArgument):
            exc.original = BadArgument
            await ctx.send('I can\'t find that member here')
    
    @command(name='poke')
    async def poke_member(self, ctx, member: Member):
        await ctx.send(f'_pokes {member.mention}_')

    @poke_member.error
    async def poke_member_error(self, ctx, exc):
        if isinstance(exc, BadArgument):
            exc.original = BadArgument
            await ctx.send('I can\'t find that member here')
    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('fun')

def setup(bot):
    bot.add_cog(Fun(bot))