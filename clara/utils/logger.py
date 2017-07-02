import logging
import sys

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

fh = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
fh.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(fh)

ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
logger.addHandler(ch)