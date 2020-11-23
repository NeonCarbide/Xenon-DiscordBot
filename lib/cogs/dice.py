from random import randint

from discord.ext.commands import command
from discord.ext.commands import Cog

class Dice(Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @command(name='dice', aliases=['roll', 'r'])
    async def roll_dice(self, ctx, dice_formula: str):
        dice, value = (val for val in dice_formula.split('d'))

        dice = (1 if not dice else int(dice))
        value = (100 if value == '%' else int(value))

        if dice <= 20: 
            rolls = [randint(1, value) for i in range(dice)]

            await ctx.send(f'{ctx.author.display_name} rolled **{dice_formula}**')
            await ctx.send(f'**{sum(rolls)}** :: **{"** + **".join([str(r) for r in rolls])}**')
        else:
            await ctx.send('Too many dice to roll')
    
    @command(name='coin', aliases=['flip', 'cf'])
    async def flip_coin(self, ctx):
        await ctx.send(f'{ctx.author.display_name} has flipped a coin')
        await ctx.send(f'It landed on **{("heads" if randint(1, 2) == 2 else "tails")}**')
    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('dice')

def setup(bot):
    bot.add_cog(Dice(bot))