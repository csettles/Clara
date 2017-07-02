from clara import clara
from clara import logger
from clara.utils.settings import TOKEN

initial_extensions = {
    'clara.cogs.overwatch',
    'clara.cogs.extras',
}

if __name__ == '__main__':
    # load extension modules
    for extension in initial_extensions:
        try:
            clara.load_extension(extension)
        except Exception as e:
            logger.error('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))


    logger.info('Waking up bot...')
    clara.run(TOKEN)
    logger.info('The bot is shut down.')
