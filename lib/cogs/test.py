from typing import Optional
from random import randint


from discord.ext.commands.errors import BadArgument, MissingAnyRole, MissingRequiredArgument
from discord.ext.commands import command
from discord.ext.commands import Cog
from discord.errors import HTTPException
from discord import Member


class Test(Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @command(name='test', aliases=['t'])
    async def test_command(self, ctx):
        await ctx.send(f'This test command was run by {ctx.author.mention}')
    
    @command(name='dice', aliases=['roll', 'r'])
    async def roll_dice(self, ctx, dice_formula: str):
        dice, value = (int(val) for val in dice_formula.split('d'))

        if dice <= 20: 
            rolls = [randint(1, value) for i in range(dice)]

            await ctx.send(f'**{dice_formula}** :: **{sum(rolls)}**')
            await ctx.send(' + '.join([str(r) for r in rolls]))
        else:
            await ctx.send('Too many dice to roll')

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
            self.bot.cogs_ready.ready_up('test')

def setup(bot):
    bot.add_cog(Test(bot))