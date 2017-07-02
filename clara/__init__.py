from .bot import Clara
from .utils import settings
from .utils.logger import logger

clara = Clara(command_prefix="!", description=settings.DESCRIPTION)

@clara.event
async def on_ready():
    logger.info('Logged in as {} with id {}'.format(clara.user.name, clara.user.id))

@clara.event
async def on_resume():
    logger.info('Resuming the bot after failure to connect...')

@clara.event
async def on_message(message):
    if message.author.bot:
        return

    await clara.process_commands(message)

# custom checker for the commands.ext module
def is_owner():
    def predicate(ctx):
        return ctx.message.author.id == "172187265433337857"
    return commands.check(predicate)