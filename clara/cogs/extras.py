from discord.ext.commands import command
import random

class Extras:
    '''A class to handle add-on, miscellaneous functions'''

    def __init__(self, bot):
        self.bot = bot

    @command(pass_context=True)
    async def hello(self, ctx):
        member = ctx.message.author
        name = member.nick if member.nick is not None else member.name
        return await self.bot.say("Hello, {}".format(name))

    @command()
    async def ping(self):
        return await self.bot.say('PONG')

    @command()
    async def roll(self, num_sides=6):
        try:
            num_sides = int(num_sides)
        except ValueError:
            return await self.bot.say("Please choose a valid number of sides for the dice.")
        num = random.randrange(1, num_sides+1)
        return await self.bot.say("I rolled a {}".format(num))

    @command()
    async def flip(self):
        coin = random.choice(['I flipped *heads*', 'I flipped *tails*'])
        return await self.bot.say(coin)

def setup(bot):
    bot.add_cog(Extras(bot))