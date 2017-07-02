from discord.ext.commands import group
from discord import Embed

player_stats = \
'''Tier:\t\t\t\t  {}
Rank:\t\t\t\t{}
Level:\t\t\t\t{}
Win Rate:\t\t{}%
Wins:\t\t\t\t{}
Ties:\t\t\t\t  {}
Losses:\t\t\t  {}'''

class OverWatch:
    '''A class for polling the OverWatch API for game stats'''

    def __init__(self, bot):
        self.bot = bot

    @group(pass_context=True)
    async def overwatch(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('Invalid overwatch command passed...')

    @overwatch.command(pass_context=True)
    async def register(self, ctx, player):
        user_id = ctx.message.author.id

        redis = await self.bot.get_redis()
        await redis.set('overwatch:{}'.format(user_id), player)

        return await self.bot.say('Registered {0.mention} as {1}'.format(ctx.message.author, player))

    @overwatch.command(pass_context=True)
    async def stats(self, ctx, player=None):
        if player is None:
            user = ctx.message.author

            redis = await self.bot.get_redis()
            player = await redis.get("overwatch:{}".format(user.id), encoding='utf-8')

            if player is None:
                return await self.bot.say('Please specify a player or register your battle tag with `!overwatch register [battle_tag]`')
        
        js = await self._get_ow_data(player, 'stats')

        if js is not None:
            stats = js['us']['stats']['competitive']['overall_stats']
            
            e = self._create_stat_embed(player, stats)

            await self.bot.say("Here's what I found...")
            await self.bot.say(embed=e)
        else:
            await self.bot.say("Sorry, I couldn't find that player 😔")

    # str str -> dict
    # returns the json dump from the OWAPI with queries player and category 
    async def _get_ow_data(self, player, category):
        player.replace("#", "-")  # compatibility purposes for GET parameters
        api_request = 'https://owapi.net/api/v3/u/{}/{}'.format(player, category)
        headers = {'User-Agent': self.bot.description}
        async with self.bot.http.session.get(api_request, headers=headers) as r:
            if r.status == 200:
                return await r.json()

    # str dict -> discord.Embed
    def _create_stat_embed(self, player, stats)
        global player_stats
        e = Embed(colour=0xf1c40f)
                e.set_thumbnail(url=stats['avatar'])
                e.set_footer(text='This data is scraped from playoverwatch.com using the Overwatch API.')
                string = player_stats.format(stats['tier'].title(),  # capitalizes first letter of string
                                            stats['comprank'],
                                            int(stats['prestige']) * 100 + int(stats['level']),
                                            stats['win_rate'],
                                            stats['wins'],
                                            stats['ties'],
                                            stats['losses'])
                e.add_field(inline='False', name="Statistics ({})".format(player.replace("-", "#")), value=string)


def setup(bot):
    bot.add_cog(OverWatch(bot))